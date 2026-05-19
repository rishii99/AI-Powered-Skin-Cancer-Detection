from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Header
from fastapi.security import OAuth2PasswordBearer
from typing import List
from app.services.auth_service import register_user, authenticate_user, create_user_token
from app.services.model_service import predict
from app.services.db import predictions_collection, feedback_collection, users_collection
from app.schemas.user import UserRegister, UserLogin, UserProfile
from app.schemas.predict import PredictionResponse, FeedbackRequest
from app.core.config import settings
from app.core.security import decode_access_token
from bson import ObjectId
import datetime

api_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = decode_access_token(token)
        user_id = payload.get('sub')
        if not user_id:
            raise HTTPException(status_code=401, detail='Invalid authentication credentials')
        user = users_collection.find_one({'_id': ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        user['id'] = str(user['_id'])
        return user
    except Exception:
        raise HTTPException(status_code=401, detail='Invalid token')


@api_router.post('/register')
def register(payload: UserRegister):
    try:
        user = register_user(payload.email, payload.password, payload.name)
        return {'message': 'User registered successfully', 'user': {'id': user['_id'], 'email': user['email']}}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@api_router.post('/login')
def login(payload: UserLogin):
    user = authenticate_user(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    token = create_user_token(user)
    return {'access_token': token, 'token_type': 'bearer'}


@api_router.get('/me', response_model=UserProfile)
def me(current_user: dict = Depends(get_current_user)):
    return {'id': current_user['id'], 'name': current_user['name'], 'email': current_user['email'], 'role': current_user.get('role', 'user')}


@api_router.post('/predict', response_model=PredictionResponse)
def predict_single(image: UploadFile = File(...), authorization: str = Header(...), current_user: dict = Depends(get_current_user)):
    if image.content_type not in settings.allowed_image_types:
        raise HTTPException(status_code=400, detail='Only JPG and PNG images are supported')
    image_bytes = image.file.read()
    if len(image_bytes) > settings.max_upload_size:
        raise HTTPException(status_code=400, detail='Image exceeds maximum allowed size')
    if len(image_bytes) == 0:
        raise HTTPException(status_code=400, detail='Image data is empty or invalid')
    result = predict(image_bytes)
    document = {
        'user_id': current_user['id'],
        'label': result['primary']['label'],
        'confidence': result['primary']['confidence'],
        'risk_level': result['risk_level'],
        'predictions': result['predictions'],
        'uncertain': result['uncertain'],
        'created_at': datetime.datetime.utcnow(),
    }
    prediction_id = predictions_collection.insert_one(document).inserted_id
    result['id'] = str(prediction_id)
    return result


@api_router.post('/predict/batch')
def predict_batch(images: List[UploadFile] = File(...), authorization: str = Header(...), current_user: dict = Depends(get_current_user)):
    responses = []
    for image in images:
        if image.content_type not in settings.allowed_image_types:
            continue
        result = predict(image.file.read())
        responses.append(result)
    return {'results': responses}


@api_router.get('/classes')
def get_classes():
    return {'classes': [
        'melanocytic_nevus',
        'melanoma',
        'benign_keratosis',
        'basal_cell_carcinoma',
        'actinic_keratosis',
        'vascular_lesion',
        'dermatofibroma'
    ]}


@api_router.get('/history')
def get_history(current_user: dict = Depends(get_current_user)):
    records = predictions_collection.find({'user_id': current_user['id']}).sort('created_at', -1).limit(50)
    return [{'id': str(item['_id']), 'label': item['label'], 'confidence': item['confidence'], 'risk_level': item['risk_level'], 'uncertain': item['uncertain'], 'created_at': item['created_at']} for item in records]


@api_router.post('/feedback')
def send_feedback(payload: FeedbackRequest, current_user: dict = Depends(get_current_user)):
    feedback_collection.insert_one({
        'prediction_id': payload.prediction_id,
        'helpful': payload.helpful,
        'comments': payload.comments,
        'user_id': current_user['id'],
        'created_at': datetime.datetime.utcnow()
    })
    return {'message': 'Feedback recorded'}

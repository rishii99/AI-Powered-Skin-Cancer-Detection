import { Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import Upload from './pages/Upload'
import Results from './pages/Results'
import History from './pages/History'
import About from './pages/About'
import Login from './pages/Login'
import Register from './pages/Register'

function App() {
  return (
    <div className="app-shell">
      <nav className="nav-bar">
        <Link to="/">Home</Link>
        <Link to="/upload">Upload</Link>
        <Link to="/history">History</Link>
        <Link to="/about">About AI</Link>
        <Link to="/login">Login</Link>
        <Link to="/register">Register</Link>
      </nav>
      <main className="app-main">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/results" element={<Results />} />
          <Route path="/history" element={<History />} />
          <Route path="/about" element={<About />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </main>
    </div>
  )
}

export default App

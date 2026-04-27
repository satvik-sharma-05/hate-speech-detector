import { useState } from 'react'
import axios from 'axios'
import './App.css'

// Use environment variable or default to localhost
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
    const [text, setText] = useState('')
    const [result, setResult] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [showAbout, setShowAbout] = useState(false)
    const [showDeveloper, setShowDeveloper] = useState(false)

    const handleSubmit = async (e) => {
        e.preventDefault()

        if (!text.trim()) {
            setError('Please enter some text')
            return
        }

        setLoading(true)
        setError(null)
        setResult(null)

        try {
            const response = await axios.post(`${API_URL}/predict`, {
                text: text
            })
            setResult(response.data)
        } catch (err) {
            setError(err.response?.data?.detail || 'An error occurred. Please try again.')
        } finally {
            setLoading(false)
        }
    }

    const handleClear = () => {
        setText('')
        setResult(null)
        setError(null)
    }

    const getResultColor = (prediction) => {
        switch (prediction) {
            case 'hate speech':
                return '#ef4444'
            case 'offensive language':
                return '#f59e0b'
            case 'neither':
                return '#10b981'
            default:
                return '#6b7280'
        }
    }

    const formatPercentage = (value) => {
        return (value * 100).toFixed(2)
    }

    return (
        <div className="app">
            <div className="container">
                <header className="header">
                    <h1>🛡️ Hate Speech Detection</h1>
                    <p>Analyze text for hate speech, offensive language, or neutral content</p>
                </header>

                <form onSubmit={handleSubmit} className="form">
                    <div className="input-group">
                        <label htmlFor="text-input">Enter text to analyze:</label>
                        <textarea
                            id="text-input"
                            value={text}
                            onChange={(e) => setText(e.target.value)}
                            placeholder="Type or paste your text here..."
                            rows="6"
                            disabled={loading}
                        />
                    </div>

                    <div className="button-group">
                        <button type="submit" disabled={loading || !text.trim()} className="btn btn-primary">
                            {loading ? 'Analyzing...' : 'Analyze Text'}
                        </button>
                        <button type="button" onClick={handleClear} disabled={loading} className="btn btn-secondary">
                            Clear
                        </button>
                    </div>
                </form>

                {error && (
                    <div className="alert alert-error">
                        <span>⚠️</span>
                        <p>{error}</p>
                    </div>
                )}

                {result && (
                    <div className="results">
                        <h2>Analysis Results</h2>

                        <div className="result-card">
                            <div className="result-header">
                                <h3>Classification</h3>
                                <span
                                    className="result-badge"
                                    style={{ backgroundColor: getResultColor(result.prediction) }}
                                >
                                    {result.prediction.toUpperCase()}
                                </span>
                            </div>

                            <div className="confidence">
                                <p>Confidence: <strong>{formatPercentage(result.confidence)}%</strong></p>
                            </div>

                            <div className="probabilities">
                                <h4>Detailed Probabilities</h4>
                                <div className="prob-list">
                                    <div className="prob-item">
                                        <div className="prob-label">
                                            <span className="prob-icon hate">🚫</span>
                                            <span>Hate Speech</span>
                                        </div>
                                        <div className="prob-bar-container">
                                            <div
                                                className="prob-bar hate"
                                                style={{ width: `${formatPercentage(result.probabilities.hate_speech)}%` }}
                                            />
                                        </div>
                                        <span className="prob-value">{formatPercentage(result.probabilities.hate_speech)}%</span>
                                    </div>

                                    <div className="prob-item">
                                        <div className="prob-label">
                                            <span className="prob-icon offensive">⚠️</span>
                                            <span>Offensive Language</span>
                                        </div>
                                        <div className="prob-bar-container">
                                            <div
                                                className="prob-bar offensive"
                                                style={{ width: `${formatPercentage(result.probabilities.offensive_language)}%` }}
                                            />
                                        </div>
                                        <span className="prob-value">{formatPercentage(result.probabilities.offensive_language)}%</span>
                                    </div>

                                    <div className="prob-item">
                                        <div className="prob-label">
                                            <span className="prob-icon neither">✅</span>
                                            <span>Neither</span>
                                        </div>
                                        <div className="prob-bar-container">
                                            <div
                                                className="prob-bar neither"
                                                style={{ width: `${formatPercentage(result.probabilities.neither)}%` }}
                                            />
                                        </div>
                                        <span className="prob-value">{formatPercentage(result.probabilities.neither)}%</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {/* About Section */}
                <div className="about-section">
                    <button
                        className="about-toggle"
                        onClick={() => setShowAbout(!showAbout)}
                    >
                        {showAbout ? '▼' : '▶'} How It Works - Technology Behind the Scenes
                    </button>

                    {showAbout && (
                        <div className="about-content">
                            <div className="about-grid">
                                <div className="about-card">
                                    <h3>🧠 Machine Learning Model</h3>
                                    <ul>
                                        <li><strong>Architecture:</strong> Bidirectional LSTM Neural Network</li>
                                        <li><strong>Embedding Dimension:</strong> 128</li>
                                        <li><strong>Layers:</strong> 2 Bidirectional LSTM layers (64 & 32 units)</li>
                                        <li><strong>Regularization:</strong> Dropout (0.3) to prevent overfitting</li>
                                        <li><strong>Output:</strong> 3-class classification (Softmax)</li>
                                        <li><strong>Training:</strong> 24,783 tweets with class balancing</li>
                                    </ul>
                                </div>

                                <div className="about-card">
                                    <h3>🔧 Text Preprocessing</h3>
                                    <ul>
                                        <li><strong>Step 1:</strong> Convert to lowercase</li>
                                        <li><strong>Step 2:</strong> Remove URLs, mentions (@), hashtags (#)</li>
                                        <li><strong>Step 3:</strong> Keep only alphabetic characters</li>
                                        <li><strong>Step 4:</strong> Remove extra whitespace</li>
                                        <li><strong>Step 5:</strong> Tokenization (10,000 vocab size)</li>
                                        <li><strong>Step 6:</strong> Padding to 50 tokens</li>
                                    </ul>
                                </div>

                                <div className="about-card">
                                    <h3>⚙️ Backend Technology</h3>
                                    <ul>
                                        <li><strong>Framework:</strong> FastAPI (Python)</li>
                                        <li><strong>ML Library:</strong> TensorFlow/Keras</li>
                                        <li><strong>Model Size:</strong> 17 MB</li>
                                        <li><strong>Response Time:</strong> &lt;500ms</li>
                                        <li><strong>API:</strong> RESTful with automatic documentation</li>
                                        <li><strong>Deployment:</strong> Optimized for 512MB memory</li>
                                    </ul>
                                </div>

                                <div className="about-card">
                                    <h3>🎨 Frontend Technology</h3>
                                    <ul>
                                        <li><strong>Framework:</strong> React 18</li>
                                        <li><strong>Build Tool:</strong> Vite</li>
                                        <li><strong>Styling:</strong> Modern CSS with animations</li>
                                        <li><strong>HTTP Client:</strong> Axios</li>
                                        <li><strong>Features:</strong> Real-time analysis, visual feedback</li>
                                        <li><strong>Design:</strong> Responsive & mobile-friendly</li>
                                    </ul>
                                </div>

                                <div className="about-card">
                                    <h3>📊 Model Performance</h3>
                                    <ul>
                                        <li><strong>Training Method:</strong> Class weights for imbalanced data</li>
                                        <li><strong>Optimizer:</strong> Adam (learning rate: 0.001)</li>
                                        <li><strong>Loss Function:</strong> Sparse Categorical Crossentropy</li>
                                        <li><strong>Early Stopping:</strong> Patience of 5 epochs</li>
                                        <li><strong>Validation:</strong> 10% validation split</li>
                                        <li><strong>Batch Size:</strong> 64</li>
                                    </ul>
                                </div>

                                <div className="about-card">
                                    <h3>🚀 Deployment</h3>
                                    <ul>
                                        <li><strong>Backend:</strong> Render (Cloud Platform)</li>
                                        <li><strong>Frontend:</strong> Vercel (Edge Network)</li>
                                        <li><strong>CI/CD:</strong> Automatic deployment from GitHub</li>
                                        <li><strong>Monitoring:</strong> Health checks & logging</li>
                                        <li><strong>Scalability:</strong> Auto-scaling enabled</li>
                                        <li><strong>Security:</strong> CORS configured, HTTPS enabled</li>
                                    </ul>
                                </div>
                            </div>

                            <div className="tech-stack">
                                <h3>🛠️ Complete Technology Stack</h3>
                                <div className="tech-badges">
                                    <span className="tech-badge">Python</span>
                                    <span className="tech-badge">TensorFlow</span>
                                    <span className="tech-badge">Keras</span>
                                    <span className="tech-badge">FastAPI</span>
                                    <span className="tech-badge">React</span>
                                    <span className="tech-badge">Vite</span>
                                    <span className="tech-badge">JavaScript</span>
                                    <span className="tech-badge">CSS3</span>
                                    <span className="tech-badge">Axios</span>
                                    <span className="tech-badge">LSTM</span>
                                    <span className="tech-badge">NLP</span>
                                    <span className="tech-badge">Deep Learning</span>
                                </div>
                            </div>

                            <div className="dataset-info">
                                <h3>📚 Dataset Information</h3>
                                <p>
                                    <strong>Source:</strong> Twitter Hate Speech Dataset<br />
                                    <strong>Size:</strong> 24,783 labeled tweets<br />
                                    <strong>Classes:</strong> Hate Speech (5.8%), Offensive Language (77.4%), Neither (16.8%)<br />
                                    <strong>Preprocessing:</strong> Cleaned, tokenized, and balanced using class weights
                                </p>
                            </div>
                        </div>
                    )}
                </div>

                <footer className="footer">
                    <p>Powered by LSTM Neural Network | Built with FastAPI & React</p>
                    <p className="footer-links">
                        <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer">API Docs</a>
                        {' | '}
                        <a href="https://github.com" target="_blank" rel="noopener noreferrer">GitHub</a>
                        {' | '}
                        <span className="footer-note">📚 See DEVELOPER_DOCUMENTATION.md for technical details</span>
                    </p>
                </footer>
            </div>
        </div>
    )
}

export default App

import { useEffect, useMemo, useState } from 'react'
import { api } from './services/api'
import { useAuth } from './contexts/AuthContext'

const prizeList = ['30% Off!', 'Free Shipping!', 'Mystery Box!', 'No Prize', 'Exclusive Drop!']

export default function App() {
  const { user, login, signup, logout } = useAuth()
  const [products, setProducts] = useState([])
  const [auctions, setAuctions] = useState([])
  const [category, setCategory] = useState('all')
  const [authMode, setAuthMode] = useState('login')
  const [authOpen, setAuthOpen] = useState(false)
  const [toast, setToast] = useState('')
  const [newsletterEmail, setNewsletterEmail] = useState('')
  const [loginForm, setLoginForm] = useState({ email: '', password: '' })
  const [signupForm, setSignupForm] = useState({ full_name: '', email: '', password: '' })
  const [wheelRotation, setWheelRotation] = useState(0)
  const [spinResult, setSpinResult] = useState('')
  const [spinning, setSpinning] = useState(false)

  useEffect(() => {
    loadProducts(category)
    loadAuctions()
  }, [category])

  useEffect(() => {
    if (!toast) return
    const timer = setTimeout(() => setToast(''), 2500)
    return () => clearTimeout(timer)
  }, [toast])

  async function loadProducts(selectedCategory) {
    try {
      const result = await api.getProducts(selectedCategory === 'all' ? '' : selectedCategory)
      setProducts(result)
    } catch (error) {
      setToast(error.message)
    }
  }

  async function loadAuctions() {
    try {
      const result = await api.getAuctions()
      setAuctions(result)
    } catch (error) {
      setToast(error.message)
    }
  }

  function addToCart(name) {
    setToast(`Added: ${name}`)
  }

  async function handleLogin(e) {
    e.preventDefault()
    try {
      const result = await login(loginForm)
      setAuthOpen(false)
      setLoginForm({ email: '', password: '' })
      setToast(result.message)
    } catch (error) {
      setToast(error.message)
    }
  }

  async function handleSignup(e) {
    e.preventDefault()
    try {
      const result = await signup(signupForm)
      setAuthOpen(false)
      setSignupForm({ full_name: '', email: '', password: '' })
      setToast(result.message)
    } catch (error) {
      setToast(error.message)
    }
  }

  async function handleNewsletter() {
    try {
      const result = await api.subscribe({ email: newsletterEmail })
      setNewsletterEmail('')
      setToast(result.message)
    } catch (error) {
      setToast(error.message)
    }
  }

  async function handleLogout() {
    try {
      await logout()
      setToast('Logged out successfully')
    } catch (error) {
      setToast(error.message)
    }
  }

  function spinWheel() {
    if (spinning) return
    setSpinning(true)
    setSpinResult('')

    const extra = 1800 + Math.floor(Math.random() * 360)
    const newRotation = wheelRotation + extra
    setWheelRotation(newRotation)

    setTimeout(() => {
      const index = Math.floor((((360 - (newRotation % 360)) % 360)) / (360 / prizeList.length))
      const prize = prizeList[index % prizeList.length]
      setSpinResult(prize)
      setToast(`You got: ${prize}`)
      setSpinning(false)
    }, 3100)
  }

  const auctionWithCountdown = useMemo(() => auctions.map((auction) => ({
    ...auction,
    timeLeft: formatTimeLeft(auction.ends_at),
  })), [auctions])

  useEffect(() => {
    const timer = setInterval(() => {
      setAuctions((current) => [...current])
    }, 1000)
    return () => clearInterval(timer)
  }, [])

  return (
    <>
      <nav id="navbar" className="nav">
        <div className="nav-logo">KICKS N CO</div>
        <ul className="nav-links">
          <li><a href="#products">Sneakers</a></li>
          <li><a href="#auction">Auction</a></li>
          <li><a href="#lucky">Lucky Draw</a></li>
          <li><a href="#blog">Blog</a></li>
          <li><a href="#about">About Us</a></li>
        </ul>
        {user ? (
          <div className="nav-user-actions">
            <span className="nav-user-name">Hi, {user.full_name.split(' ')[0]}</span>
            <button className="nav-cta" onClick={handleLogout}>Logout</button>
          </div>
        ) : (
          <button className="nav-cta" onClick={() => setAuthOpen(true)}>Login / Sign Up</button>
        )}
      </nav>

      <section id="hero" className="hero">
        <div className="hero-bg" />
        <div className="hero-overlay" />
        <div className="hero-content">
          <p className="hero-eyebrow">Est. 2023 · Sneaker Culture</p>
          <h1 className="hero-title">KICKS<br /><span>N CO</span></h1>
          <p className="hero-sub">Welcome to the World of Sneakers</p>
          <div className="hero-btns">
            <a className="btn-primary" href="#products">Shop Now</a>
            <a className="btn-secondary" href="#auction">Live Auctions</a>
          </div>
        </div>
      </section>

      <div className="ticker">
        <div className="ticker-inner">
          {['Nike', 'Jordan', 'Adidas', 'Converse', 'New Balance', 'Yeezy', 'Off-White', 'Travis Scott', 'Dunk Low', 'Air Max', 'Nike', 'Jordan', 'Adidas'].map((item, idx) => <span key={`${item}-${idx}`}>{item}</span>)}
        </div>
      </div>

      <section id="products" className="section dark-alt">
        <SectionHeader eyebrow="Latest Drops" title={'Shop\nSneakers'} />
        <div className="filter-bar">
          {[
            ['all', 'All'],
            ['nike', 'Nike'],
            ['jordan', 'Jordan'],
            ['adidas', 'Adidas'],
            ['new', 'New Balance'],
          ].map(([key, label]) => (
            <button key={key} className={`filter-btn ${category === key ? 'active' : ''}`} onClick={() => setCategory(key)}>{label}</button>
          ))}
        </div>

        <div className="products-grid">
          {products.map((product) => (
            <div className="product-card" key={product.id}>
              <div className="product-img">
                <img src={product.image_url} alt={product.name} loading="lazy" />
                <span className={`product-badge ${product.badge === 'HOT' ? 'hot' : ''}`}>{product.badge}</span>
              </div>
              <div className="product-info">
                <div className="product-brand">{product.brand}</div>
                <div className="product-name">{product.name}</div>
                <div className="product-footer">
                  <div>
                    <div className="product-price">${product.price}</div>
                    <div className="product-resell">Resell ~${product.resell_price}</div>
                  </div>
                  <button className="add-btn" onClick={() => addToCart(product.name)}>+</button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section id="quote" className="quote-section">
        <p className="quote-text">Sneakers are more than just shoes — they are part of the <em>family</em>, a symbol of unity, and a shared <em>passion</em>.</p>
      </section>

      <section id="auction" className="section dark-alt">
        <SectionHeader eyebrow="Live Now" title={'Live\nAuction'} />
        <div className="auction-grid">
          {auctionWithCountdown.map((auction) => (
            <div className="auction-card" key={auction.id}>
              <div className="auction-img"><img src={auction.image_url} alt={auction.name} loading="lazy" /></div>
              <div className="auction-body">
                <div className="auction-name">{auction.name}</div>
                <div className="auction-meta">
                  <div><div className="meta-label">Current Bid</div><div className="meta-val">${auction.current_bid}</div></div>
                  <div><div className="meta-label">Time Left</div><div className="meta-val time">{auction.timeLeft}</div></div>
                </div>
                <button className="bid-btn" onClick={() => setToast(`Bid placed on ${auction.name}`)}>Place Bid →</button>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section id="lucky" className="section">
        <SectionHeader eyebrow="Try your luck" title={'Lucky\nDraw'} />
        <div className="draw-container">
          <p className="muted-copy">Spin the wheel for a chance to win exclusive sneaker prizes and discounts</p>
          <div className="draw-prizes">
            {prizeList.map((prize) => <span key={prize} className="prize-chip">{prize}</span>)}
          </div>
          <div className="wheel-wrap">
            <div className="draw-pointer" />
            <div className="draw-wheel" style={{ transform: `rotate(${wheelRotation}deg)` }} />
          </div>
          <div className="draw-result">{spinResult}</div>
          <button className="draw-btn" onClick={spinWheel} disabled={spinning}>{spinning ? 'Spinning...' : 'Spin the Wheel'}</button>
        </div>
      </section>

      <section id="blog" className="section dark-alt">
        <SectionHeader eyebrow="Culture & News" title={'Latest\nStories'} />
        <div className="blog-grid">
          <div className="blog-card large">
            <img src="https://sneakernews.com/wp-content/uploads/2023/11/Willy-Wonka-Nike-Dunk-Low-Custom-Timothee-Chalamet-4.jpg.jpeg?w=780&h=548&crop=1" alt="Wonka Nike Dunk" />
            <div className="blog-info"><span className="blog-tag">Collab Drop</span><h3>Timothée Chalamet&apos;s Wonka Nike Dunk — The Real Golden Ticket</h3></div>
          </div>
          <div className="blog-side">
            <div className="blog-card"><img src="https://sneakernews.com/wp-content/uploads/2023/08/Nike-Zoom-Vomero-5-University-Red-8.jpg?w=540&h=380&crop=1" alt="Vomero" /><div className="blog-info"><span className="blog-tag">New Release</span><h3>Nike Zoom Vomero 5 "University Red" Drops Soon</h3></div></div>
            <div className="blog-card"><img src="https://sneakernews.com/wp-content/uploads/2023/11/Nike-Air-Force-1-Mid-Denim-DD9625-400-9.jpg?w=540&h=380&crop=1" alt="Air Force 1 Mid Denim" /><div className="blog-info"><span className="blog-tag">Style</span><h3>Air Force 1 Mid Gets a Denim Makeover</h3></div></div>
          </div>
        </div>
      </section>

      <section id="about" className="about-section">
        <div className="about-img">
          <img src="https://cdn.broadsheet.com.au/melbourne/images/2019/05/08/151749-1733-145030-6204-Sneaker_Con_719.jpg" alt="Sneaker convention" />
          <div className="about-accent" />
        </div>
        <div className="about-text">
          <SectionHeader eyebrow="Our Story" title={'About\nUs'} align="left" />
          <p>Welcome to KICKS N CO — your destination for all things sneakers. This full-stack build keeps the look and feel of your uploaded HTML while adding real backend APIs, PostgreSQL data, and session-based auth.</p>
          <p>Use it as a clean starting point for a sneaker marketplace, auction portal, or culture-first ecommerce brand.</p>
          <div className="about-stats">
            <Stat number="12K+" label="Happy Customers" />
            <Stat number="500+" label="Rare Pairs" />
            <Stat number="3+" label="Years Active" />
            <Stat number="100%" label="Verified Auth" />
          </div>
        </div>
      </section>

      <div className="signup-strip">
        <p>SIGN UP & GET 30% OFF YOUR FIRST PURCHASE</p>
        <div className="signup-form-inline">
          <input value={newsletterEmail} onChange={(e) => setNewsletterEmail(e.target.value)} type="email" placeholder="Enter your email" />
          <button onClick={handleNewsletter}>Subscribe</button>
        </div>
      </div>

      <footer className="footer">
        <div className="footer-top">
          <div className="footer-brand">
            <span className="nav-logo">KICKS N CO</span>
            <p>Your ultimate destination for sneaker culture — buying, selling, and celebrating the culture.</p>
          </div>
          <div className="footer-col">
            <h4>Shop</h4>
            <ul><li>Nike</li><li>Jordan</li><li>Adidas</li><li>Converse</li><li>New Balance</li></ul>
          </div>
          <div className="footer-col">
            <h4>Company</h4>
            <ul><li>About Us</li><li>Events</li><li>Achievements</li><li>Careers</li><li>Blog</li></ul>
          </div>
          <div className="footer-col">
            <h4>Contact</h4>
            <ul><li>kicksandco@yahoo.com</li><li>123-000-456</li><li>Mon–Sat 10am–8pm IST</li></ul>
          </div>
        </div>
      </footer>

      {authOpen && (
        <div className="login-overlay" onClick={(e) => e.target.className === 'login-overlay' && setAuthOpen(false)}>
          <div className="auth-modal">
            <button className="modal-close" onClick={() => setAuthOpen(false)}>✕</button>
            <div className="auth-tabs">
              <button className={`auth-tab ${authMode === 'login' ? 'active' : ''}`} onClick={() => setAuthMode('login')}>Log In</button>
              <button className={`auth-tab ${authMode === 'signup' ? 'active' : ''}`} onClick={() => setAuthMode('signup')}>Sign Up</button>
            </div>

            {authMode === 'login' ? (
              <form className="auth-form active" onSubmit={handleLogin}>
                <input type="email" placeholder="Email Address" value={loginForm.email} onChange={(e) => setLoginForm({ ...loginForm, email: e.target.value })} />
                <input type="password" placeholder="Password" value={loginForm.password} onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })} />
                <button type="submit" className="auth-submit">Log In</button>
              </form>
            ) : (
              <form className="auth-form active" onSubmit={handleSignup}>
                <input type="text" placeholder="Full Name" value={signupForm.full_name} onChange={(e) => setSignupForm({ ...signupForm, full_name: e.target.value })} />
                <input type="email" placeholder="Email Address" value={signupForm.email} onChange={(e) => setSignupForm({ ...signupForm, email: e.target.value })} />
                <input type="password" placeholder="Create Password" value={signupForm.password} onChange={(e) => setSignupForm({ ...signupForm, password: e.target.value })} />
                <button type="submit" className="auth-submit">Create Account</button>
              </form>
            )}
          </div>
        </div>
      )}

      {toast && <div className="toast show">{toast}</div>}
    </>
  )
}

function SectionHeader({ eyebrow, title, align = 'center' }) {
  return (
    <div className="section-header" style={{ textAlign: align }}>
      <span className="section-eyebrow">{eyebrow}</span>
      <h2 className="section-title">{title.split('\n').map((line) => <span key={line}>{line}<br /></span>)}</h2>
    </div>
  )
}

function Stat({ number, label }) {
  return <div className="stat"><div className="stat-num">{number}</div><div className="stat-label">{label}</div></div>
}

function formatTimeLeft(dateString) {
  const diff = Math.max(0, Math.floor((new Date(dateString).getTime() - Date.now()) / 1000))
  const hours = Math.floor(diff / 3600)
  const minutes = Math.floor((diff % 3600) / 60)
  const seconds = diff % 60
  return `${hours}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
}

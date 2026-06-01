import { useState, useEffect, useCallback, useRef, useMemo } from 'react'
import { Search, SlidersHorizontal, Star, X, ChevronLeft, ChevronRight, Filter, Leaf, Building2, TreePine, Recycle, Award, ChevronDown, ChevronUp, MapPin, Package, Sparkles, ArrowUpDown } from 'lucide-react'

const BASE = window.__BACKEND_URL__ || '';

async function apiFetch(path, opts = {}) {
  for (let i = 0; i < 5; i++) {
    try {
      const r = await fetch(BASE + path, opts);
      if (r.ok) return r.json();
    } catch (_) {}
    await new Promise(r => setTimeout(r, 1500));
  }
  return null;
}

function useCSS() {
  useEffect(() => {
    if (document.getElementById('greenloop-styles')) return;
    const style = document.createElement('style');
    style.id = 'greenloop-styles';
    style.textContent = ':root { --accent: #00C9A7; --accent2: #1E3A5F; }';
      document.head.appendChild(style);
  }, []);
}

const suppliers = [
  { id: 1, name: 'EcoFarm Organics', rating: 4.8, reviews: 124, price: '$12.50/kg', category: 'Agriculture', certifications: ['USDA Organic', 'Fair Trade'], image: '🌱', location: 'California, USA' },
  { id: 2, name: 'GreenPack Solutions', rating: 4.6, reviews: 89, price: '$0.85/unit', category: 'Packaging', certifications: ['FSC Certified', 'Carbon Neutral'], image: '📦', location: 'Berlin, Germany' },
  { id: 3, name: 'SolarTech Industries', rating: 4.9, reviews: 203, price: '$2,400/kW', category: 'Energy', certifications: ['ISO 14001', 'Cradle to Cradle'], image: '☀️', location: 'Shenzhen, China' },
  { id: 4, name: 'PureWater Systems', rating: 4.7, reviews: 156, price: '$8.20/unit', category: 'Water', certifications: ['WaterSense', 'B Corp'], image: '💧', location: 'Amsterdam, Netherlands' },
  { id: 5, name: 'CarbonClear Credits', rating: 4.5, reviews: 67, price: '$45/ton', category: 'Carbon Offsets', certifications: ['VERRA', 'Gold Standard'], image: '🌳', location: 'London, UK' },
  { id: 6, name: 'BioMatter Materials', rating: 4.4, reviews: 42, price: '$3.20/kg', category: 'Materials', certifications: ['Cradle to Cradle', 'OK compost'], image: '🧫', location: 'Tokyo, Japan' },
  { id: 7, name: 'WasteNot Recycling', rating: 4.3, reviews: 78, price: '$0.50/kg', category: 'Waste', certifications: ['Zero Waste', 'EcoVadis'], image: '♻️', location: 'Toronto, Canada' },
  { id: 8, name: 'GreenLogistics Co', rating: 4.6, reviews: 134, price: '$5.75/km', category: 'Logistics', certifications: ['Carbon Neutral', 'Green Freight'], image: '🚚', location: 'Singapore' },
  { id: 9, name: 'AgriNova BioTech', rating: 4.7, reviews: 95, price: '$22.00/L', category: 'Agriculture', certifications: ['USDA Organic', 'Non-GMO'], image: '🧬', location: 'Sao Paulo, Brazil' },
  { id: 10, name: 'EcoTextile Mills', rating: 4.2, reviews: 56, price: '$18.50/m', category: 'Textiles', certifications: ['GOTS', 'OEKO-TEX'], image: '🧵', location: 'Mumbai, India' },
  { id: 11, name: 'Sustainable Timber', rating: 4.8, reviews: 88, price: '$650/m³', category: 'Materials', certifications: ['FSC Certified', 'PEFC'], image: '🪵', location: 'Vancouver, Canada' },
  { id: 12, name: 'CleanChem Solutions', rating: 4.1, reviews: 34, price: '$95.00/kg', category: 'Chemicals', certifications: ['Cradle to Cradle', 'EU Ecolabel'], image: '🧪', location: 'Basel, Switzerland' },
]

const categories = ['All', 'Agriculture', 'Packaging', 'Energy', 'Water', 'Carbon Offsets', 'Materials', 'Waste', 'Logistics', 'Textiles', 'Chemicals']

function Sidebar({ filters, setFilters, isOpen, setIsOpen }) {
  return (
    <>
      <aside className={`w-64 flex-shrink-0 flex flex-col border-r border-white/5 bg-white/[0.02] h-full ${isOpen ? 'block' : 'hidden'} lg:block`}>
        <div className="p-4 border-b border-white/5">
          <div className="flex items-center gap-2 text-emerald-400">
            <Leaf className="w-5 h-5" />
            <span className="font-semibold">GreenLoop Connect</span>
          </div>
        </div>
        <nav className="flex-1 p-4 space-y-6 overflow-y-auto">
          <div>
            <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">Categories</h3>
            <div className="space-y-1">
              {categories.map(cat => (
                <button
                  key={cat}
                  onClick={() => setFilters(prev => ({ ...prev, category: cat }))}
                  className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-all duration-200 ${
                    filters.category === cat ? 'bg-emerald-500/10 text-emerald-300 border border-emerald-500/20' : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
                  }`}
                >
                  {cat}
                </button>
              ))}
            </div>
          </div>
          <div>
            <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">Price Range</h3>
            <div className="space-y-4 px-1">
              <input
                type="range"
                min="0"
                max="100"
                value={filters.priceMax}
                onChange={e => setFilters(prev => ({ ...prev, priceMax: Number(e.target.value) }))}
                className="w-full accent-emerald-500"
              />
              <div className="flex justify-between text-xs text-slate-500">
                <span>$0</span>
                <span>${filters.priceMax === 100 ? '5000+' : filters.priceMax * 50}</span>
              </div>
            </div>
          </div>
          <div>
            <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">Minimum Rating</h3>
            <div className="flex gap-1">
              {[1,2,3,4,5].map(star => (
                <button
                  key={star}
                  onClick={() => setFilters(prev => ({ ...prev, minRating: prev.minRating === star ? 0 : star }))}
                  className={`p-1 rounded transition-colors ${filters.minRating >= star ? 'text-amber-400' : 'text-slate-600'}`}
                >
                  <Star className="w-4 h-4 fill-current" />
                </button>
              ))}
            </div>
          </div>
        </nav>
      </aside>
      {isOpen && <div className="fixed inset-0 bg-black/50 z-10 lg:hidden" onClick={() => setIsOpen(false)} />}
    </>
  )
}

function FeaturedCarousel({ suppliers }) {
  const [currentIndex, setCurrentIndex] = useState(0)
  const featured = (suppliers || []).filter(s => s.rating >= 4.7).slice(0, 6)

  useEffect(() => {
    if (featured.length === 0) return;
    const interval = setInterval(() => {
      setCurrentIndex(prev => (prev + 1) % featured.length)
    }, 4000)
    return () => clearInterval(interval)
  }, [featured.length])

  if (featured.length === 0) return null

  const handlePrev = () => setCurrentIndex(prev => (prev - 1 + featured.length) % featured.length)
  const handleNext = () => setCurrentIndex(prev => (prev + 1) % featured.length)

  return (
    <div className="relative mb-6 overflow-hidden rounded-xl glass p-4">
      <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4 flex items-center gap-2">
        <Sparkles className="w-4 h-4 text-amber-400" />
        Featured Suppliers
      </h3>
      <div className="relative">
        {featured.map((supplier, idx) => (
          <div
            key={supplier.id}
            className={`transition-all duration-500 absolute inset-0 ${
              idx === currentIndex ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-8'
            }`}
            style={{ position: idx === currentIndex ? 'relative' : 'absolute' }}
          >
            {idx === currentIndex && (
              <div className="flex items-center gap-4 p-3 rounded-lg bg-white/5">
                <span className="text-4xl">{supplier.image}</span>
                <div className="flex-1 min-w-0">
                  <h4 className="text-lg font-semibold text-slate-100">{supplier.name}</h4>
                  <div className="flex items-center gap-2 text-sm text-slate-400">
                    <MapPin className="w-3 h-3" />
                    {supplier.location}
                  </div>
                  <div className="flex items-center gap-3 mt-1">
                    <div className="flex items-center gap-1 text-amber-400">
                      <Star className="w-3 h-3 fill-current" />
                      <span className="text-sm">{supplier.rating}</span>
                    </div>
                    <span className="text-emerald-400 font-semibold">{supplier.price}</span>
                  </div>
                </div>
                <div className="hidden sm:flex gap-2 flex-wrap">
                  {(supplier.certifications || []).slice(0, 2).map(cert => (
                    <span key={cert} className="px-2 py-1 text-xs rounded-full bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
                      {cert}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
      <div className="flex justify-center gap-2 mt-3">
        <button onClick={handlePrev} className="p-1 rounded hover:bg-white/10 transition-colors">
          <ChevronLeft className="w-4 h-4 text-slate-400" />
        </button>
        <div className="flex gap-1 items-center">
          {featured.map((_, idx) => (
            <button
              key={idx}
              onClick={() => setCurrentIndex(idx)}
              className={`w-2 h-2 rounded-full transition-all duration-300 ${
                idx === currentIndex ? 'bg-emerald-400 w-4' : 'bg-slate-600'
              }`}
            />
          ))}
        </div>
        <button onClick={handleNext} className="p-1 rounded hover:bg-white/10 transition-colors">
          <ChevronRight className="w-4 h-4 text-slate-400" />
        </button>
      </div>
    </div>
  )
}

function SupplierCard({ supplier, onQuickView }) {
  return (
    <div
      onClick={() => onQuickView(supplier)}
      className="glass p-4 fade-in hover-card cursor-pointer transition-all duration-200"
    >
      <div className="flex items-start justify-between mb-3">
        <span className="text-4xl">{supplier.image}</span>
        <button className="p-1.5 rounded-lg hover:bg-white/10 transition-colors" onClick={e => { e.stopPropagation(); onQuickView(supplier) }}>
          <Search className="w-4 h-4 text-slate-500" />
        </button>
      </div>
      <h3 className="text-base font-semibold text-slate-100 mb-1 truncate">{supplier.name}</h3>
      <div className="flex items-center gap-2 text-xs text-slate-500 mb-2">
        <MapPin className="w-3 h-3" />
        <span className="truncate">{supplier.location}</span>
      </div>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-1 text-amber-400">
          <Star className="w-3.5 h-3.5 fill-current" />
          <span className="text-sm font-medium text-slate-200">{supplier.rating}</span>
          <span className="text-xs text-slate-500">({supplier.reviews})</span>
        </div>
        <span className="text-emerald-400 font-semibold text-sm">{supplier.price}</span>
      </div>
      <div className="flex flex-wrap gap-1.5">
        {(supplier.certifications || []).slice(0, 2).map(cert => (
          <span key={cert} className="px-2 py-0.5 text-[10px] rounded-full bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
            {cert}
          </span>
        ))}
        {(supplier.certifications || []).length > 2 && (
          <span className="px-2 py-0.5 text-[10px] rounded-full bg-white/5 text-slate-400">+{supplier.certifications.length - 2}</span>
        )}
      </div>
    </div>
  )
}

function QuickViewModal({ supplier, onClose }) {
  if (!supplier) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm" onClick={onClose}>
      <div className="glass p-6 max-w-lg w-full max-h-[80vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center gap-3">
            <span className="text-5xl">{supplier.image}</span>
            <div>
              <h2 className="text-xl font-semibold text-slate-100">{supplier.name}</h2>
              <div className="flex items-center gap-1 text-amber-400">
                <Star className="w-4 h-4 fill-current" />
                <span className="text-sm text-slate-200">{supplier.rating} ({supplier.reviews} reviews)</span>
              </div>
            </div>
          </div>
          <button onClick={onClose} className="p-1 rounded hover:bg-white/10 transition-colors">
            <X className="w-5 h-5 text-slate-400" />
          </button>
        </div>
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-3">
            <div className="glass p-3">
              <p className="text-xs text-slate-500 mb-1">Category</p>
              <p className="text-sm font-medium text-slate-200">{supplier.category}</p>
            </div>
            <div className="glass p-3">
              <p className="text-xs text-slate-500 mb-1">Price</p>
              <p className="text-sm font-medium text-emerald-400">{supplier.price}</p>
            </div>
            <div className="glass p-3">
              <p className="text-xs text-slate-500 mb-1">Location</p>
              <p className="text-sm font-medium text-slate-200">{supplier.location}</p>
            </div>
            <div className="glass p-3">
              <p className="text-xs text-slate-500 mb-1">Certifications</p>
              <div className="flex flex-wrap gap-1 mt-1">
                {(supplier.certifications || []).map(cert => (
                  <span key={cert} className="px-2 py-0.5 text-[10px] rounded-full bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
                    {cert}
                  </span>
                ))}
              </div>
            </div>
          </div>
          <div className="flex gap-3">
            <button className="flex-1 px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-sm transition-colors">
              Contact Supplier
            </button>
            <button className="flex-1 px-4 py-2 rounded-lg bg-white/10 hover:bg-white/15 text-slate-200 font-medium text-sm transition-colors border border-white/10">
              Request Quote
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

function Pagination({ currentPage, totalPages, onPageChange }) {
  const pages = []
  const startPage = Math.max(1, currentPage - 2)
  const endPage = Math.min(totalPages, currentPage + 2)
  for (let i = startPage; i <= endPage; i++) pages.push(i)

  return (
    <div className="flex items-center justify-center gap-2 mt-6">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="p-2 rounded-lg hover:bg-white/10 transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
      >
        <ChevronLeft className="w-4 h-4" />
      </button>
      {startPage > 1 && (
        <>
          <button onClick={() => onPageChange(1)} className="px-3 py-1.5 rounded-lg text-sm text-slate-400 hover:bg-white/10 transition-colors">1</button>
          {startPage > 2 && <span className="text-slate-500">...</span>}
        </>
      )}
      {pages.map(page => (
        <button
          key={page}
          onClick={() => onPageChange(page)}
          className={`px-3 py-1.5 rounded-lg text-sm transition-all duration-200 ${
            page === currentPage ? 'bg-emerald-500/10 text-emerald-300 border border-emerald-500/20' : 'text-slate-400 hover:bg-white/10'
          }`}
        >
          {page}
        </button>
      ))}
      {endPage < totalPages && (
        <>
          {endPage < totalPages - 1 && <span className="text-slate-500">...</span>}
          <button onClick={() => onPageChange(totalPages)} className="px-3 py-1.5 rounded-lg text-sm text-slate-400 hover:bg-white/10 transition-colors">{totalPages}</button>
        </>
      )}
      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="p-2 rounded-lg hover:bg-white/10 transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
      >
        <ChevronRight className="w-4 h-4" />
      </button>
    </div>
  )
}

export default function App() {
  useCSS()
  const [searchQuery, setSearchQuery] = useState('')
  const [filters, setFilters] = useState({ category: 'All', priceMax: 100, minRating: 0 })
  const [sortBy, setSortBy] = useState('name')
  const [sortDir, setSortDir] = useState('asc')
  const [currentPage, setCurrentPage] = useState(1)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [quickViewSupplier, setQuickViewSupplier] = useState(null)
  const [toast, setToast] = useState(null)
  const itemsPerPage = 6

  const filteredSuppliers = useMemo(() => {
    let result = [...suppliers]
    if (searchQuery) {
      const q = searchQuery.toLowerCase()
      result = result.filter(s => s.name.toLowerCase().includes(q) || s.category.toLowerCase().includes(q) || s.location.toLowerCase().includes(q))
    }
    if (filters.category !== 'All') {
      result = result.filter(s => s.category === filters.category)
    }
    if (filters.minRating > 0) {
      result = result.filter(s => s.rating >= filters.minRating)
    }
    if (filters.priceMax < 100) {
      const maxPrice = filters.priceMax * 50
      result = result.filter(s => {
        const price = parseFloat(s.price.replace(/[$,]/g, ''))
        return price <= maxPrice
      })
    }
    result.sort((a, b) => {
      let valA, valB
      if (sortBy === 'name') { valA = a.name; valB = b.name }
      else if (sortBy === 'rating') { valA = a.rating; valB = b.rating }
      else if (sortBy === 'price') { 
        valA = parseFloat(a.price.replace(/[$,]/g, ''))
        valB = parseFloat(b.price.replace(/[$,]/g, ''))
      }
      else { valA = a.name; valB = b.name }
      if (typeof valA === 'string') {
        return sortDir === 'asc' ? valA.localeCompare(valB) : valB.localeCompare(valA)
      }
      return sortDir === 'asc' ? valA - valB : valB - valA
    })
    return result
  }, [searchQuery, filters, sortBy, sortDir])

  const totalPages = Math.ceil(filteredSuppliers.length / itemsPerPage)
  const paginatedSuppliers = filteredSuppliers.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage)

  const handleSort = (field) => {
    if (sortBy === field) {
      setSortDir(prev => prev === 'asc' ? 'desc' : 'asc')
    } else {
      setSortBy(field)
      setSortDir('asc')
    }
  }

  const showToast = (message) => {
    setToast(message)
    setTimeout(() => setToast(null), 3000)
  }

  return (
    <div className="flex h-screen overflow-hidden bg-[#06080f] text-slate-100 font-[Inter]">
      <Sidebar filters={filters} setFilters={setFilters} isOpen={sidebarOpen} setIsOpen={setSidebarOpen} />
      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="h-14 flex items-center justify-between px-6 border-b border-white/5 flex-shrink-0">
          <div className="flex items-center gap-4 flex-1">
            <button className="lg:hidden p-2 rounded-lg hover:bg-white/10 transition-colors" onClick={() => setSidebarOpen(true)}>
              <Filter className="w-4 h-4 text-slate-400" />
            </button>
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
              <input
                type="text"
                placeholder="Search suppliers, categories, locations..."
                value={searchQuery}
                onChange={e => { setSearchQuery(e.target.value); setCurrentPage(1) }}
                className="w-full pl-10 pr-4 py-2 bg-white/5 border border-white/10 rounded-lg text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-emerald-500/50 focus:ring-1 focus:ring-emerald-500/30 transition-all"
              />
            </div>
          </div>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 text-sm text-slate-400">
              <span>Sort:</span>
              <button onClick={() => handleSort('name')} className={`px-2 py-1 rounded text-xs ${sortBy === 'name' ? 'text-emerald-300 bg-emerald-500/10' : 'hover:text-slate-200'}`}>
                Name {sortBy === 'name' && (sortDir === 'asc' ? '↑' : '↓')}
              </button>
              <button onClick={() => handleSort('rating')} className={`px-2 py-1 rounded text-xs ${sortBy === 'rating' ? 'text-emerald-300 bg-emerald-500/10' : 'hover:text-slate-200'}`}>
                Rating {sortBy === 'rating' && (sortDir === 'asc' ? '↑' : '↓')}
              </button>
              <button onClick={() => handleSort('price')} className={`px-2 py-1 rounded text-xs ${sortBy === 'price' ? 'text-emerald-300 bg-emerald-500/10' : 'hover:text-slate-200'}`}>
                Price {sortBy === 'price' && (sortDir === 'asc' ? '↑' : '↓')}
              </button>
            </div>
          </div>
        </header>
        <main className="flex-1 overflow-y-auto p-6">
          <div className="max-w-7xl mx-auto">
            <div className="mb-6">
              <h1 className="text-2xl font-bold gradient-text">GreenLoop Connect Marketplace</h1>
              <p className="text-slate-400 text-sm mt-1">Find certified green suppliers and offset your carbon footprint in one trusted marketplace</p>
            </div>
            
            <FeaturedCarousel suppliers={suppliers} />
            
            <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
              {(paginatedSuppliers || []).map(supplier => (
                <SupplierCard key={supplier.id} supplier={supplier} onQuickView={setQuickViewSupplier} />
              ))}
            </div>
            
            {filteredSuppliers.length === 0 && (
              <div className="text-center py-12">
                <Package className="w-12 h-12 text-slate-600 mx-auto mb-3" />
                <p className="text-slate-400">No suppliers match your criteria</p>
                <button 
                  onClick={() => { setSearchQuery(''); setFilters({ category: 'All', priceMax: 100, minRating: 0 }); setCurrentPage(1) }}
                  className="mt-3 px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-sm transition-colors"
                >
                  Clear Filters
                </button>
              </div>
            )}
            
            {filteredSuppliers.length > 0 && (
              <Pagination currentPage={currentPage} totalPages={totalPages} onPageChange={setCurrentPage} />
            )}
          </div>
        </main>
      </div>
      
      {quickViewSupplier && (
        <QuickViewModal supplier={quickViewSupplier} onClose={() => setQuickViewSupplier(null)} />
      )}
      
      {toast && (
        <div className="fixed bottom-6 right-6 z-50 glass p-4 fade-in">
          <div className="flex items-center gap-3">
            <Award className="w-5 h-5 text-emerald-400" />
            <p className="text-sm text-slate-200">{toast}</p>
          </div>
        </div>
      )}
    </div>
  )
}
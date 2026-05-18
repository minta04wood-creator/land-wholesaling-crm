import React, { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Search, MapPin, Building2, Phone, Mail, DollarSign, LayoutDashboard, CheckCircle2, ChevronRight, FileText, Globe, AlertTriangle, Columns, LayoutGrid, Menu, X, Sun, Moon, ChevronDown, Share2, Link2, Bell, BellOff, StickyNote } from 'lucide-react'
import { useSwipeable } from 'react-swipeable'
import { DealNotes } from './DealNotes'
import { generateBuyerDealSheet, copyShareableLink } from './ShareSheet'
import { DragDropContext, Droppable, Draggable, DropResult } from '@hello-pangea/dnd'
import { deals } from './data'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'

// Fix Leaflet icons
import iconUrl from 'leaflet/dist/images/marker-icon.png'
import iconShadow from 'leaflet/dist/images/marker-shadow.png'
let DefaultIcon = L.icon({ iconUrl, shadowUrl: iconShadow, iconAnchor: [12, 41] })
L.Marker.prototype.options.icon = DefaultIcon

const MapView = React.lazy(() => import('./MapView'))
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Button } from '@/components/ui/button'

const COLUMNS = ['New Lead', 'Contacted', 'Negotiating', 'Under Contract', 'Closed']
const COLUMN_COLORS: Record<string, string> = {
  'New Lead': 'bg-blue-500',
  'Contacted': 'bg-amber-500',
  'Negotiating': 'bg-purple-500',
  'Under Contract': 'bg-orange-500',
  'Closed': 'bg-emerald-500',
}

export const calculateDealScore = (deal: any, rData?: string[]) => {
  let score = 80 // Base score for making the pipeline
  if (deal.ac >= 20) score += 5 // Bonus for large acreage
  if (deal.ac >= 50) score += 5 // Huge bonus for institutional scale
  if (deal.zn.includes('M1') || deal.zn.includes('C2')) score += 5 // Bonus for commercial/industrial

  // Deduct points based on risk data (if scraped)
  if (rData && rData.length > 0) {
    if (rData[0] && !rData[0].includes("No")) score -= 20 // Severe flood risk
    if (rData[1] && !rData[1].includes("No")) score -= 15 // Title issues
    if (rData[2] && !rData[2].includes("Unrestricted")) score -= 10 // Zoning issues
  }
  
  return Math.min(100, Math.max(0, score))
}

export default function App() {
  const [search, setSearch] = useState('')
  const [selectedDeal, setSelectedDeal] = useState<any>(null)
  const [copiedId, setCopiedId] = useState<string | null>(null)
  const [filterMode, setFilterMode] = useState<'all' | 'vacant' | 'institutional'>('all')
  const [viewMode, setViewMode] = useState<'grid' | 'kanban' | 'map'>('kanban')
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [theme, setTheme] = useState<'dark' | 'light'>(() =>
    (localStorage.getItem('crm-theme') as 'dark' | 'light') || 'dark'
  )

  useEffect(() => {
    localStorage.setItem('crm-theme', theme)
    document.documentElement.classList.toggle('dark', theme === 'dark')
  }, [theme])

  // Push notification permission
  const [notifPermission, setNotifPermission] = useState<NotificationPermission>(
    'Notification' in window ? Notification.permission : 'denied'
  )
  const requestNotifications = async () => {
    if (!('Notification' in window)) return
    const permission = await Notification.requestPermission()
    setNotifPermission(permission)
    if (permission === 'granted') {
      new Notification('Land CRM', { body: 'Notifications enabled! You\'ll be alerted on deal updates.', icon: '/favicon.svg' })
    }
  }
  const sendNotification = (title: string, body: string) => {
    if (notifPermission === 'granted') {
      new Notification(title, { body, icon: '/favicon.svg' })
    }
  }

  const [linkCopied, setLinkCopied] = useState(false)



  // Pipeline State
  const [pipeline, setPipeline] = useState<Record<string, any[]>>(() => {
    const saved = localStorage.getItem('land-pipeline')
    const defaultPipeline = { 'New Lead': deals, 'Contacted': [], 'Negotiating': [], 'Under Contract': [], 'Closed': [] }
    if (saved) {
      try {
        const parsed = JSON.parse(saved)
        // Ensure all deals from the static data.ts exist in some pipeline column
        const existingIds = new Set()
        COLUMNS.forEach(col => {
          if (parsed[col]) {
            parsed[col].forEach((d: any) => existingIds.add(d.n))
          }
        })
        
        // Find missing deals and add to 'New Lead'
        const missingDeals = deals.filter(d => !existingIds.has(d.n))
        if (missingDeals.length > 0) {
          parsed['New Lead'] = [...(parsed['New Lead'] || []), ...missingDeals]
        }
        return parsed
      } catch (e) {
        console.error("Error loading saved pipeline:", e)
        return defaultPipeline
      }
    }
    return defaultPipeline
  })

  // Mocked Server States
  const [riskData, setRiskData] = useState<Record<string, string[]>>({})
  const [buyerIntel, setBuyerIntel] = useState<Record<string, string>>({})
  const [scraperLogs, setScraperLogs] = useState<Record<string, any>>({})
  const [loadingAction, setLoadingAction] = useState<string | null>(null)

  useEffect(() => {
    localStorage.setItem('land-pipeline', JSON.stringify(pipeline))
  }, [pipeline])


  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text)
    setCopiedId(id)
    setTimeout(() => setCopiedId(null), 2000)
  }

  const formatMoney = (val: number) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(val)

  const onDragEnd = (result: DropResult) => {
    const { source, destination } = result;
    if (!destination) return;
    if (source.droppableId === destination.droppableId && source.index === destination.index) return;
    const sourceList = Array.from(pipeline[source.droppableId]);
    const destList = source.droppableId === destination.droppableId ? sourceList : Array.from(pipeline[destination.droppableId]);
    const [moved] = sourceList.splice(source.index, 1);
    if (source.droppableId === destination.droppableId) {
      sourceList.splice(destination.index, 0, moved);
      setPipeline({ ...pipeline, [source.droppableId]: sourceList });
    } else {
      destList.splice(destination.index, 0, moved);
      setPipeline({ ...pipeline, [source.droppableId]: sourceList, [destination.droppableId]: destList });
    }
  }

  // Mobile-friendly: move deal to a different stage without dragging
  const moveDeal = (deal: any, fromColumn: string, toColumn: string) => {
    if (fromColumn === toColumn) return
    const sourceList = pipeline[fromColumn].filter((d: any) => d.n !== deal.n)
    const destList = [...pipeline[toColumn], deal]
    setPipeline({ ...pipeline, [fromColumn]: sourceList, [toColumn]: destList })
  }

  // Find which column a deal is currently in
  const getDealColumn = (deal: any): string => {
    for (const col of COLUMNS) {
      if (pipeline[col]?.find((d: any) => d.n === deal.n)) return col
    }
    return 'New Lead'
  }



  const generatePSA = async (deal: any) => {
    const { default: jsPDF } = await import('jspdf')
    const doc = new jsPDF()
    doc.setFont("times", "bold")
    doc.setFontSize(18)
    doc.text("PURCHASE AND SALE AGREEMENT", 105, 20, { align: "center" })
    
    doc.setFontSize(12)
    doc.setFont("times", "normal")
    const date = new Date().toLocaleDateString()
    doc.text(`Date: ${date}`, 20, 40)
    doc.text(`SELLER: ${deal.seller}`, 20, 50)
    doc.text(`BUYER: Institutional Land Acquisitions LLC (and/or assigns)`, 20, 60)
    
    doc.text("1. PROPERTY DESCRIPTION:", 20, 80)
    doc.text(`Address: ${deal.addr}, ${deal.city}, GA ${deal.zp}`, 30, 90)
    doc.text(`Parcel ID: ${deal.n} | Acreage: ${deal.ac} Acres`, 30, 100)
    
    doc.text("2. PURCHASE PRICE:", 20, 120)
    doc.text(`The Buyer agrees to pay ${formatMoney(deal.lv * 0.55)} for the Property.`, 30, 130)

    doc.text("3. CLOSING:", 20, 150)
    doc.text("Closing shall occur within 30 days of the Effective Date.", 30, 160)
    
    doc.text("____________________________           ____________________________", 20, 200)
    doc.text("Seller Signature                            Buyer Signature", 25, 210)
    
    doc.save(`PSA_Deal_${deal.n}.pdf`)
  }

  const runExaSearch = async (deal: any) => {
    setLoadingAction('exa')
    try {
      const res = await fetch(`http://localhost:8000/api/intel?buyer=${encodeURIComponent(deal.b1n)}`)
      const data = await res.json()
      setBuyerIntel({
        ...buyerIntel,
        [deal.n]: data.intel || "Error retrieving intel."
      })
    } catch (e) {
      console.error(e)
      setBuyerIntel({
        ...buyerIntel,
        [deal.n]: "Could not connect to the real backend. Make sure the FastAPI server is running on localhost:8000."
      })
    }
    setLoadingAction(null)
  }

  const runRiskCheck = async (deal: any) => {
    setLoadingAction('risk')
    try {
      const res = await fetch(`http://localhost:8000/api/risk?ac=${deal.ac}&zn=${encodeURIComponent(deal.zn)}`)
      const data = await res.json()
      setRiskData({
        ...riskData,
        [deal.n]: data.risks || ["Error retrieving risk data."]
      })
      if (data.risks && data.risks.length > 0) {
        sendNotification('Risk Alert', `New risks identified for ${deal.ac} acres in ${deal.city}`)
      }
    } catch (e) {
      console.error(e)
      setRiskData({
        ...riskData,
        [deal.n]: ["Could not connect to backend."]
      })
    }
    setLoadingAction(null)
  }

  const runAdvancedScrapers = async (deal: any) => {
    setLoadingAction('scrape')
    try {
      // Mocked backend call for Apify and Firecrawl integration
      await new Promise(r => setTimeout(r, 2000))
      setScraperLogs({
        ...scraperLogs,
        [deal.n]: [
          { id: 1, tool: "Firecrawl", icon: "🔥", target: "County Tax Assessor Website", result: "Extracted 12 pages of property records. No hidden liens detected. Last sale was in 2012 for $120,000." },
          { id: 2, tool: "Apify", icon: "🤖", target: "LinkedIn & Social Footprint", result: "Found 3 profiles for 'Director of Land Acquisitions' at " + deal.b1n + ". Buyer is highly active." },
          { id: 3, tool: "Exa", icon: "🌐", target: "Zoning Board Minutes", result: "Recent mention of upcoming sewer line extension exactly 0.5 miles from this parcel. Massive upzoning potential." }
        ]
      })
    } catch (e) {
      console.error(e)
    }
    setLoadingAction(null)
  }

  const getFilteredList = (list: any[]) => {
    let result = list;
    if (filterMode === 'vacant') result = result.filter(d => d.zn.includes('R') || d.ac > 5)
    if (filterMode === 'institutional') result = result.filter(d => d.b1n.includes('LLC') || d.b1n.includes('INC') || d.b1n.includes('PARTNERS'))
    
    return result.filter(d => 
      d.city.toLowerCase().includes(search.toLowerCase()) || 
      d.seller.toLowerCase().includes(search.toLowerCase()) || 
      d.b1n.toLowerCase().includes(search.toLowerCase()) ||
      d.zn.toLowerCase().includes(search.toLowerCase())
    )
  }

  // Rough geocoding for demo (defaults near Atlanta/Gwinnett)
  const mapCenter: [number, number] = [33.9526, -84.0077]

  return (
    <>
    <div className={`min-h-screen flex transition-colors duration-500 ${theme === 'dark' ? 'dark bg-[#0a0b14]' : 'bg-slate-50'}`}>
      {/* Sidebar - Studio Style */}
      <aside className={`fixed inset-y-0 left-0 z-50 w-20 md:w-64 glass-panel border-r transition-all duration-500 transform ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} md:translate-x-0`}>
        <div className="h-full flex flex-col p-4">
          <div className="flex items-center gap-3 px-2 mb-10 mt-2">
            <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center shadow-lg shadow-primary/20 shrink-0">
              <Globe className="w-6 h-6 text-primary-foreground" />
            </div>
            <div className="hidden md:block">
              <h1 className="text-lg font-black tracking-tighter font-studio">LAND<span className="text-primary">CRM</span></h1>
              <p className="text-[10px] font-bold text-muted-foreground uppercase tracking-[0.2em]">Institutional</p>
            </div>
          </div>

          <nav className="flex-1 space-y-1.5">
            {[
              { id: 'kanban', icon: LayoutDashboard, label: 'Pipeline' },
              { id: 'inventory', icon: Columns, label: 'Inventory' },
              { id: 'map', icon: Globe, label: 'GIS Map' },
              { id: 'analytics', icon: CheckCircle2, label: 'Reporting' },
            ].map(item => (
              <button
                key={item.id}
                onClick={() => setViewMode(item.id as any)}
                className={`w-full flex items-center gap-3 px-3 py-3 rounded-xl transition-all duration-200 group ${
                  viewMode === item.id 
                  ? 'bg-primary text-primary-foreground shadow-md shadow-primary/10' 
                  : 'text-muted-foreground hover:bg-accent hover:text-foreground'
                }`}
              >
                <item.icon className={`w-5 h-5 shrink-0 ${viewMode === item.id ? 'scale-110' : 'group-hover:scale-110'} transition-transform`} />
                <span className="hidden md:block font-semibold text-sm">{item.label}</span>
              </button>
            ))}
          </nav>

          <div className="mt-auto p-4 bg-primary/5 rounded-2xl border border-primary/10 hidden md:block">
            <p className="text-[10px] font-black text-primary uppercase tracking-widest mb-1">Scraper Status</p>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span className="text-[11px] font-bold opacity-80">All MCPs Online</span>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className={`flex-1 flex flex-col transition-all duration-500 ${sidebarOpen ? 'md:ml-64' : 'ml-0 md:ml-64'}`}>
        {/* Topbar */}
        <header className="h-20 flex items-center justify-between px-6 md:px-10 glass-panel border-b sticky top-0 z-40">
          <div className="flex items-center gap-6 flex-1">
            <button onClick={() => setSidebarOpen(!sidebarOpen)} className="md:hidden">
              <Menu className="w-6 h-6" />
            </button>
            <div className="relative w-full max-w-md group hidden md:block">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground transition-colors group-focus-within:text-primary" />
              <input
                type="text"
                placeholder="Quick search properties (Cmd+K)"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full h-11 pl-11 pr-4 rounded-xl bg-secondary/50 border border-border/50 focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all font-medium text-sm"
              />
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1.5 mr-4 px-3 py-1.5 rounded-full bg-secondary/50 border border-border/40 hidden lg:flex">
              <div className="w-2 h-2 rounded-full bg-amber-500" />
              <span className="text-[11px] font-black uppercase tracking-tight">{deals.length} Active Deals</span>
            </div>
            
            <Button variant="ghost" size="icon" className="rounded-xl" onClick={() => setTheme(t => t === 'dark' ? 'light' : 'dark')}>
              {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </Button>
            <Button variant="ghost" size="icon" className="rounded-xl relative" onClick={requestNotifications}>
              {notifPermission === 'granted' ? <Bell className="w-5 h-5 text-primary" /> : <BellOff className="w-5 h-5" />}
              {notifPermission === 'granted' && <span className="absolute top-2.5 right-2.5 w-2 h-2 bg-red-500 rounded-full border-2 border-background" />}
            </Button>
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-primary to-indigo-600 flex items-center justify-center text-white font-black text-xs shadow-lg shadow-primary/20 cursor-pointer hover:scale-105 transition-transform">
              MW
            </div>
          </div>
        </header>

        {/* Content Area */}
        <div className="flex-1 p-6 md:p-10 overflow-x-hidden bg-background/50">
          {viewMode === 'kanban' ? (
            <DragDropContext onDragEnd={onDragEnd}>
              <div className="flex h-full gap-8 overflow-x-auto pb-10 scrollbar-hide">
                {COLUMNS.map(columnId => (
                  <div key={columnId} className="flex flex-col w-[320px] shrink-0 h-full">
                    <div className="flex items-center justify-between mb-5 px-1 shrink-0">
                      <div className="flex items-center gap-2.5">
                        <div className={`w-2.5 h-2.5 rounded-full ${COLUMN_COLORS[columnId]} shadow-[0_0_12px_rgba(0,0,0,0.1)]`} />
                        <h2 className="text-sm font-black uppercase tracking-[0.15em] font-studio opacity-90">{columnId}</h2>
                      </div>
                      <Badge variant="secondary" className="rounded-md font-mono text-[10px] px-2 py-0.5 opacity-60">
                        {pipeline[columnId].length}
                      </Badge>
                    </div>
                    
                    <Droppable droppableId={columnId}>
                      {(provided, snapshot) => (
                        <div
                          {...provided.droppableProps}
                          ref={provided.innerRef}
                          className={`stage-tray transition-colors ${snapshot.isDraggingOver ? 'bg-primary/5 ring-1 ring-primary/20 shadow-inner' : ''}`}
                        >
                          <div className="space-y-4">
                            {getFilteredList(pipeline[columnId]).map((deal, index) => (
                              <Draggable key={deal.n.toString()} draggableId={deal.n.toString()} index={index}>
                                {(provided, snapshot) => (
                                  <div
                                    ref={provided.innerRef}
                                    {...provided.draggableProps}
                                    {...provided.dragHandleProps}
                                    className={`${snapshot.isDragging ? 'z-50' : ''}`}
                                  >
                                    <DealCard
                                      deal={deal}
                                      handleCopy={handleCopy}
                                      copiedId={copiedId}
                                      riskData={riskData[deal.n]}
                                      currentColumn={columnId}
                                      moveDeal={moveDeal}
                                      onOpen={() => setSelectedDeal(deal)}
                                    />
                                  </div>
                                )}
                              </Draggable>
                            ))}
                            {provided.placeholder}
                          </div>
                        </div>
                      )}
                    </Droppable>
                  </div>
                ))}
              </div>
            </DragDropContext>
          ) : viewMode === 'map' ? (
            <React.Suspense fallback={<div className="w-full h-full flex items-center justify-center font-bold text-muted-foreground animate-pulse">Loading Map Engine...</div>}>
              <MapView deals={getFilteredList(deals)} onSelectDeal={setSelectedDeal} />
            </React.Suspense>
          ) : (
            <div className="p-4 md:p-8">
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 md:gap-6">
                {getFilteredList(deals).map(deal => (
                  <div key={deal.n}>
                    <DealCard deal={deal} handleCopy={handleCopy} copiedId={copiedId} riskData={riskData[deal.n]} onOpen={() => setSelectedDeal(deal)} />
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Full Screen Deal Modal */}
      <Dialog open={!!selectedDeal} onOpenChange={() => setSelectedDeal(null)}>
        <DialogContent className="max-w-7xl w-full h-[95dvh] md:h-[90vh] p-0 flex flex-col bg-background/95 backdrop-blur-3xl border-white/10 shadow-[0_0_100px_rgba(0,0,0,0.5)] overflow-hidden">
          {selectedDeal && (
            <div className="flex flex-col md:flex-row h-full w-full overflow-hidden">
              {/* Left Column - Deal Details & Actions */}
              <div className="flex-1 flex flex-col md:min-w-[60%] md:border-r border-white/10 overflow-hidden">
                <div className="p-4 md:p-8 border-b border-white/10 bg-gradient-to-r from-primary/10 to-transparent shrink-0">
                  <div className="flex flex-wrap items-center justify-between gap-4">
                    <div>
                      <div className="flex items-center gap-3 mb-3">
                        <Badge className="bg-primary text-primary-foreground font-mono">DEAL #{selectedDeal.n}</Badge>
                        <Badge variant="outline" className="border-white/20 text-white/70">{selectedDeal.zn}</Badge>
                        <Badge className="bg-emerald-500/20 text-emerald-400 border-none hover:bg-emerald-500/30">
                          {formatMoney(selectedDeal.lv * 0.15)} EST PROFIT
                        </Badge>
                        <Badge className={`border-none ${calculateDealScore(selectedDeal, riskData[selectedDeal.n]) > 80 ? 'bg-primary/20 text-primary' : calculateDealScore(selectedDeal, riskData[selectedDeal.n]) > 60 ? 'bg-amber-500/20 text-amber-500' : 'bg-destructive/20 text-destructive-foreground'}`}>
                          SCORE: {calculateDealScore(selectedDeal, riskData[selectedDeal.n])}/100
                        </Badge>
                      </div>
                      <DialogTitle className="text-2xl md:text-4xl font-black tracking-tight text-white flex items-center gap-3">
                        {selectedDeal.ac} Acres <span className="text-muted-foreground font-medium text-lg md:text-2xl">in {selectedDeal.city}, GA</span>
                      </DialogTitle>
                    </div>
                    <div className="flex gap-2 flex-wrap">
                      <Button variant="default" className="bg-emerald-600 hover:bg-emerald-700 text-white" onClick={() => generatePSA(selectedDeal)}>
                        <FileText className="w-4 h-4 mr-2" /> PSA
                      </Button>
                      <Button variant="outline" className="border-purple-500/50 text-purple-400 hover:bg-purple-500/10" onClick={() => generateBuyerDealSheet(selectedDeal)}>
                        <Share2 className="w-4 h-4 mr-2" /> Deal Sheet
                      </Button>
                      <Button variant="outline" className="border-blue-500/50 text-blue-400 hover:bg-blue-500/10" onClick={() => {
                        copyShareableLink(selectedDeal)
                        setLinkCopied(true)
                        setTimeout(() => setLinkCopied(false), 2000)
                      }}>
                        <Link2 className="w-4 h-4 mr-2" /> {linkCopied ? 'Copied!' : 'Copy Link'}
                      </Button>
                    </div>
                  </div>
                </div>

                <Tabs defaultValue="outreach" className="flex-1 flex flex-col min-h-0">
                  <div className="px-8 border-b border-white/10 bg-black/20 shrink-0">
                    <TabsList className="w-full justify-start rounded-none border-b-0 bg-transparent p-0 h-14 overflow-x-auto">
                      <TabsTrigger value="outreach" className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent data-[state=active]:text-primary px-4 md:px-6 h-full font-bold uppercase tracking-wider text-xs whitespace-nowrap">Pitch & Scripts</TabsTrigger>
                      <TabsTrigger value="intel" className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent data-[state=active]:text-primary px-4 md:px-6 h-full font-bold uppercase tracking-wider text-xs whitespace-nowrap">Buyer Intel</TabsTrigger>
                      <TabsTrigger value="risk" className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent data-[state=active]:text-primary px-4 md:px-6 h-full font-bold uppercase tracking-wider text-xs whitespace-nowrap">Risk & Env</TabsTrigger>
                      <TabsTrigger value="notes" className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent data-[state=active]:text-primary px-4 md:px-6 h-full font-bold uppercase tracking-wider text-xs whitespace-nowrap">
                        <StickyNote className="w-3.5 h-3.5 mr-1.5" />Notes
                      </TabsTrigger>
                      <TabsTrigger value="scrapers" className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent data-[state=active]:text-primary px-4 md:px-6 h-full font-bold uppercase tracking-wider text-xs whitespace-nowrap">Deep Scrape</TabsTrigger>
                    </TabsList>
                  </div>

                  <ScrollArea className="flex-1 bg-black/10">
                    <div className="p-8">
                      <TabsContent value="outreach" className="mt-0 space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
                        {/* Seller Contact Block */}
                        <div>
                          <p className="text-[10px] font-black uppercase tracking-[0.2em] text-amber-500/60 mb-3">📞 Seller Contact</p>
                          <div className="bg-amber-500/10 border border-amber-500/20 p-6 rounded-2xl space-y-3">
                            <div className="flex items-center justify-between">
                              <h3 className="text-xl font-bold text-amber-500 flex items-center gap-2"><Building2 className="w-5 h-5" /> {selectedDeal.seller}</h3>
                              <Button size="sm" className="bg-amber-500 hover:bg-amber-600 text-amber-950 font-bold" onClick={() => handleCopy(selectedDeal.sph, 'modal-phone')}>
                                {copiedId === 'modal-phone' ? 'Copied!' : 'Copy Phone'}
                              </Button>
                            </div>
                            {selectedDeal.sloc && <p className="text-xs text-amber-500/60 font-medium">📍 {selectedDeal.sloc}</p>}
                            <div className="flex flex-wrap items-center gap-4 text-sm">
                              <a href={`tel:${selectedDeal.sph}`} className="flex items-center gap-2 text-amber-500/80 hover:text-amber-400 transition-colors">
                                <Phone className="w-4 h-4" /> {selectedDeal.sph}
                              </a>
                              {(selectedDeal.sem || selectedDeal.semail) && (
                                <a href={`mailto:${selectedDeal.sem || selectedDeal.semail}`} className="flex items-center gap-2 text-amber-500/80 hover:text-amber-400 transition-colors">
                                  <Mail className="w-4 h-4" /> {selectedDeal.sem || selectedDeal.semail}
                                </a>
                              )}
                            </div>
                            {selectedDeal.held && <p className="text-xs text-amber-500/50 mt-1">🕐 Held: {selectedDeal.held}</p>}
                          </div>
                        </div>
                        <div className="bg-card/50 border border-white/5 rounded-2xl p-6 shadow-inner">
                          <p className="text-[10px] font-black uppercase tracking-[0.2em] text-muted-foreground mb-3">Seller Call Script</p>
                          <p className="text-lg leading-relaxed text-foreground/90 font-serif whitespace-pre-line">{selectedDeal.ss.replace(/\\n/g, '\n')}</p>
                        </div>

                        {/* Leverage */}
                        {selectedDeal.lev && (
                          <div className="bg-yellow-500/5 border border-yellow-500/20 rounded-2xl p-5 flex items-start gap-3">
                            <AlertTriangle className="w-5 h-5 text-yellow-500 shrink-0 mt-0.5" />
                            <div>
                              <p className="text-[10px] font-black uppercase tracking-[0.2em] text-yellow-500/60 mb-1">Leverage / Motivation</p>
                              <p className="text-sm text-yellow-200/90 font-medium">{selectedDeal.lev}</p>
                            </div>
                          </div>
                        )}
                        
                        {/* Primary Buyer Contact Block */}
                        <div className="mt-12">
                          <p className="text-[10px] font-black uppercase tracking-[0.2em] text-blue-400/60 mb-3">🎯 Primary Buyer</p>
                          <div className="bg-blue-500/10 border border-blue-500/20 p-6 rounded-2xl space-y-3">
                            <div className="flex items-center justify-between">
                              <h3 className="text-xl font-bold text-blue-400 flex items-center gap-2"><Building2 className="w-5 h-5" /> {selectedDeal.b1n}</h3>
                              <Button size="sm" className="bg-blue-500 hover:bg-blue-600 text-blue-950 font-bold" onClick={() => handleCopy(selectedDeal.b1p, 'modal-buyer-phone')}>
                                {copiedId === 'modal-buyer-phone' ? 'Copied!' : 'Copy Phone'}
                              </Button>
                            </div>
                            <div className="flex flex-wrap items-center gap-4 text-sm">
                              <a href={`tel:${selectedDeal.b1p}`} className="flex items-center gap-2 text-blue-400/80 hover:text-blue-300 transition-colors">
                                <Phone className="w-4 h-4" /> {selectedDeal.b1p}
                              </a>
                              {selectedDeal.b1e && (
                                <a href={`mailto:${selectedDeal.b1e}`} className="flex items-center gap-2 text-blue-400/80 hover:text-blue-300 transition-colors">
                                  <Mail className="w-4 h-4" /> {selectedDeal.b1e}
                                </a>
                              )}
                            </div>
                          </div>
                        </div>
                        <div className="bg-card/50 border border-white/5 rounded-2xl p-6 shadow-inner">
                          <p className="text-[10px] font-black uppercase tracking-[0.2em] text-muted-foreground mb-3">Buyer Pitch Script</p>
                          <p className="text-lg leading-relaxed text-foreground/90 font-serif whitespace-pre-line">{selectedDeal.bs.replace(/\\n/g, '\n')}</p>
                        </div>

                        {/* Secondary Buyer Contact Block */}
                        {selectedDeal.b2n && (
                          <div className="mt-8">
                            <p className="text-[10px] font-black uppercase tracking-[0.2em] text-purple-400/60 mb-3">🔄 Secondary Buyer</p>
                            <div className="bg-purple-500/10 border border-purple-500/20 p-6 rounded-2xl space-y-3">
                              <div className="flex items-center justify-between">
                                <h3 className="text-lg font-bold text-purple-400 flex items-center gap-2"><Building2 className="w-5 h-5" /> {selectedDeal.b2n}</h3>
                                <Button size="sm" variant="outline" className="border-purple-500/50 text-purple-400 hover:bg-purple-500/10 font-bold" onClick={() => handleCopy(selectedDeal.b2p, 'modal-buyer2-phone')}>
                                  {copiedId === 'modal-buyer2-phone' ? 'Copied!' : 'Copy Phone'}
                                </Button>
                              </div>
                              <div className="flex flex-wrap items-center gap-4 text-sm">
                                <a href={`tel:${selectedDeal.b2p}`} className="flex items-center gap-2 text-purple-400/80 hover:text-purple-300 transition-colors">
                                  <Phone className="w-4 h-4" /> {selectedDeal.b2p}
                                </a>
                                {selectedDeal.b2e && (
                                  <a href={`mailto:${selectedDeal.b2e}`} className="flex items-center gap-2 text-purple-400/80 hover:text-purple-300 transition-colors">
                                    <Mail className="w-4 h-4" /> {selectedDeal.b2e}
                                  </a>
                                )}
                              </div>
                            </div>
                          </div>
                        )}
                      </TabsContent>

                      <TabsContent value="intel" className="mt-0 space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <div className="flex justify-between items-center mb-6">
                          <div>
                            <h3 className="text-xl font-bold text-white">Dynamic Buyer Intel</h3>
                            <p className="text-muted-foreground">Powered by Exa Search MCP</p>
                          </div>
                          <Button onClick={() => runExaSearch(selectedDeal)} disabled={loadingAction === 'exa'} className="bg-indigo-600 hover:bg-indigo-700 text-white">
                            {loadingAction === 'exa' ? 'Searching Exa...' : <><Globe className="w-4 h-4 mr-2" /> Search Web</>}
                          </Button>
                        </div>
                        
                        {buyerIntel[selectedDeal.n] ? (
                           <div className="bg-indigo-500/10 border border-indigo-500/30 p-6 rounded-2xl text-indigo-200 whitespace-pre-line leading-relaxed">
                             {buyerIntel[selectedDeal.n]}
                           </div>
                        ) : (
                          <div className="flex flex-col items-center justify-center h-64 text-muted-foreground border-2 border-dashed border-white/10 rounded-2xl">
                            <Globe className="w-12 h-12 mb-4 opacity-50" />
                            <p>No intel gathered yet. Click Search Web to query Exa.</p>
                          </div>
                        )}
                      </TabsContent>

                      <TabsContent value="risk" className="mt-0 space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <div className="flex justify-between items-center mb-6">
                          <div>
                            <h3 className="text-xl font-bold text-white">Environmental & Title Risk</h3>
                            <p className="text-muted-foreground">Automated checks via Wholesaler Skill</p>
                          </div>
                          <Button onClick={() => runRiskCheck(selectedDeal)} disabled={loadingAction === 'risk'} variant="outline" className="border-red-500/50 text-red-400 hover:bg-red-500/10">
                            {loadingAction === 'risk' ? 'Scanning API...' : <><AlertTriangle className="w-4 h-4 mr-2" /> Run Check</>}
                          </Button>
                        </div>

                        {riskData[selectedDeal.n] ? (
                           <div className="space-y-4">
                             {riskData[selectedDeal.n].map((r, i) => (
                               <div key={i} className={`p-4 rounded-xl border ${r.includes('No') ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' : 'bg-red-500/10 border-red-500/30 text-red-400'} flex items-center gap-3`}>
                                 {r.includes('No') ? <CheckCircle2 className="w-5 h-5" /> : <AlertTriangle className="w-5 h-5" />}
                                 {r}
                               </div>
                             ))}
                           </div>
                        ) : (
                          <div className="flex flex-col items-center justify-center h-64 text-muted-foreground border-2 border-dashed border-white/10 rounded-2xl">
                            <AlertTriangle className="w-12 h-12 mb-4 opacity-50" />
                            <p>No risk check performed yet.</p>
                          </div>
                        )}
                      </TabsContent>

                      <TabsContent value="notes" className="mt-0 animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <div className="flex items-center justify-between mb-4">
                          <div>
                            <h3 className="text-xl font-bold">Activity Log</h3>
                            <p className="text-muted-foreground text-sm">Track every call, email, and conversation</p>
                          </div>
                        </div>
                        <DealNotes dealId={selectedDeal.n.toString()} />
                      </TabsContent>

                      <TabsContent value="scrapers" className="mt-0 space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <div className="flex justify-between items-center mb-6">
                          <div>
                            <h3 className="text-xl font-bold text-white">Deep Scraper Analysis</h3>
                            <p className="text-muted-foreground">Powered by Apify, Firecrawl & Exa MCPs</p>
                          </div>
                          <Button onClick={() => runAdvancedScrapers(selectedDeal)} disabled={loadingAction === 'scrape'} className="bg-purple-600 hover:bg-purple-700 text-white shadow-[0_0_20px_rgba(147,51,234,0.3)]">
                            {loadingAction === 'scrape' ? 'Scraping Web...' : <><Globe className="w-4 h-4 mr-2" /> Run Deep Scrape</>}
                          </Button>
                        </div>

                        {scraperLogs[selectedDeal.n] ? (
                          <Accordion type="single" collapsible className="w-full">
                            {scraperLogs[selectedDeal.n].map((log: any) => (
                              <AccordionItem key={log.id} value={`item-${log.id}`} className="border-white/10">
                                <AccordionTrigger className="text-white hover:text-purple-400">
                                  <div className="flex items-center gap-3">
                                    <span className="text-2xl">{log.icon}</span>
                                    <span className="font-bold">{log.tool}</span>
                                    <span className="text-muted-foreground font-normal text-sm">— {log.target}</span>
                                  </div>
                                </AccordionTrigger>
                                <AccordionContent className="text-purple-200/80 leading-relaxed text-sm">
                                  {log.result}
                                </AccordionContent>
                              </AccordionItem>
                            ))}
                          </Accordion>
                        ) : (
                          <div className="flex flex-col items-center justify-center h-64 text-muted-foreground border-2 border-dashed border-purple-500/20 rounded-2xl bg-purple-500/5">
                            <Globe className="w-12 h-12 mb-4 text-purple-500/50" />
                            <p>No deep scraper data found. Click Run Deep Scrape to extract.</p>
                          </div>
                        )}
                      </TabsContent>
                    </div>
                  </ScrollArea>
                </Tabs>
              </div>

              {/* Right Column - Map & Math — hidden on mobile */}
              <div className="hidden md:flex w-[40%] bg-black/40 flex-col shrink-0">
                <div className="h-2/5 border-b border-white/10 relative">
                  <MapContainer center={mapCenter} zoom={13} style={{ height: '100%', width: '100%' }}>
                    <TileLayer url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png" />
                    <Marker position={mapCenter}>
                      <Popup>{selectedDeal.addr}</Popup>
                    </Marker>
                  </MapContainer>
                  <div className="absolute top-4 right-4 z-[400]">
                    <Button variant="secondary" className="shadow-lg" onClick={() => window.open(`https://www.google.com/maps/search/${selectedDeal.addr.replace(/ /g, '+')},+${selectedDeal.city},+GA+${selectedDeal.zp}`, '_blank')}>
                       Open in Google Maps
                    </Button>
                  </div>
                </div>

                <div className="p-8 flex-1 flex flex-col justify-center space-y-6">
                  <div className="bg-white/5 border border-white/10 rounded-3xl p-8">
                    <p className="text-sm font-bold text-muted-foreground uppercase tracking-wider mb-2">Estimated Market Value</p>
                    <p className="text-4xl font-black text-white">{formatMoney(selectedDeal.lv)}</p>
                  </div>
                  <div className="bg-amber-500/10 border border-amber-500/20 rounded-3xl p-8">
                    <p className="text-sm font-bold text-amber-500/80 uppercase tracking-wider mb-2">Max Allowable Offer (55%)</p>
                    <p className="text-4xl font-black text-amber-500">{formatMoney(selectedDeal.lv * 0.55)}</p>
                  </div>
                  <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-3xl p-8 relative overflow-hidden">
                    <div className="absolute right-0 bottom-0 opacity-10"><DollarSign className="w-32 h-32" /></div>
                    <p className="text-sm font-bold text-emerald-500/80 uppercase tracking-wider mb-2 relative z-10">Target Fee (15%)</p>
                    <p className="text-5xl font-black text-emerald-400 relative z-10">{formatMoney(selectedDeal.lv * 0.15)}</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>

    {/* Mobile Bottom Nav */}
    <nav className="md:hidden fixed bottom-0 left-0 right-0 z-40 glass-panel border-t border-white/10 flex items-center justify-around px-2 pb-[env(safe-area-inset-bottom)] h-16">
      <button onClick={() => setFilterMode('all')} className={`flex flex-col items-center gap-1 px-4 py-2 rounded-xl transition-colors ${filterMode === 'all' ? 'text-primary' : 'text-muted-foreground'}`}>
        <LayoutDashboard className="w-5 h-5" />
        <span className="text-[10px] font-bold uppercase tracking-wider">All</span>
      </button>
      <button onClick={() => setFilterMode('vacant')} className={`flex flex-col items-center gap-1 px-4 py-2 rounded-xl transition-colors ${filterMode === 'vacant' ? 'text-primary' : 'text-muted-foreground'}`}>
        <MapPin className="w-5 h-5" />
        <span className="text-[10px] font-bold uppercase tracking-wider">Vacant</span>
      </button>
      <button onClick={() => setFilterMode('institutional')} className={`flex flex-col items-center gap-1 px-4 py-2 rounded-xl transition-colors ${filterMode === 'institutional' ? 'text-primary' : 'text-muted-foreground'}`}>
        <Building2 className="w-5 h-5" />
        <span className="text-[10px] font-bold uppercase tracking-wider">Institutional</span>
      </button>
      <button onClick={() => setMobileMenuOpen(v => !v)} className={`flex flex-col items-center gap-1 px-4 py-2 rounded-xl transition-colors ${mobileMenuOpen ? 'text-primary' : 'text-muted-foreground'}`}>
        <DollarSign className="w-5 h-5" />
        <span className="text-[10px] font-bold uppercase tracking-wider">Value</span>
      </button>
    </nav>
    </>
  )
}


function DealCard({ deal, handleCopy, copiedId, riskData, currentColumn, moveDeal, onOpen }: any) {
  const [stageOpen, setStageOpen] = useState(false)
  const fee = deal.lv * 0.15

  const handlers = useSwipeable({
    onSwipedLeft: () => {
      const idx = COLUMNS.indexOf(currentColumn)
      if (idx < COLUMNS.length - 1) moveDeal(deal, currentColumn, COLUMNS[idx + 1])
    },
    onSwipedRight: () => {
      const idx = COLUMNS.indexOf(currentColumn)
      if (idx > 0) moveDeal(deal, currentColumn, COLUMNS[idx - 1])
    },
    trackMouse: false,
    preventScrollOnSwipe: true
  })

  return (
    <div {...handlers} className="h-full">
      <Card 
        onClick={onOpen}
        className="premium-card h-full bg-card/40 border border-border/50 hover:border-primary/30 flex flex-col cursor-pointer group"
      >
        <CardHeader className="p-4 pb-2">
          <div className="flex justify-between items-start mb-2">
            <span className="font-mono text-[10px] text-muted-foreground opacity-50 font-bold tracking-tighter">#{deal.n}</span>
            <div className="flex gap-1.5">
              <div className={`px-1.5 py-0.5 rounded-sm text-[9px] font-black tracking-widest flex items-center justify-center ${calculateDealScore(deal, riskData) > 80 ? 'bg-primary/10 text-primary border border-primary/20' : calculateDealScore(deal, riskData) > 60 ? 'bg-amber-500/10 text-amber-500 border border-amber-500/20' : 'bg-destructive/10 text-destructive border border-destructive/20'}`}>
                SCORE: {calculateDealScore(deal, riskData)}
              </div>
              <Badge variant="outline" className="text-[10px] uppercase font-black tracking-widest border-border/60 bg-secondary/30">{deal.zn}</Badge>
            </div>
          </div>
          <CardTitle className="text-sm font-black font-studio tracking-tight leading-tight group-hover:text-primary transition-colors line-clamp-2">
            {deal.ac} Acres • {deal.city}
          </CardTitle>
          <div className="flex items-center gap-1 mt-1 text-[11px] text-muted-foreground font-medium">
            <MapPin className="w-3 h-3" />
            Gwinnett County, GA
          </div>
        </CardHeader>

        <CardContent className="p-4 pt-2 flex-1 flex flex-col">
          <div className="space-y-2 mb-4">
            {/* Stakeholders */}
            <div className="p-2 rounded-xl bg-secondary/30 border border-border/40 flex items-center justify-between group/row hover:bg-secondary/50 transition-colors">
              <div className="min-w-0">
                <p className="text-[9px] uppercase font-black text-muted-foreground/60 tracking-wider">Seller</p>
                <p className="text-xs font-bold truncate">{deal.seller}</p>
              </div>
              <Button size="icon" variant="ghost" className="h-7 w-7 rounded-lg hover:bg-primary/10 hover:text-primary opacity-0 group-hover/row:opacity-100 transition-all" onClick={e => { e.stopPropagation(); handleCopy(deal.sph, `sc-${deal.n}`) }}>
                {copiedId === `sc-${deal.n}` ? <CheckCircle2 className="w-3.5 h-3.5" /> : <Phone className="w-3.5 h-3.5" />}
              </Button>
            </div>

            <div className="p-2 rounded-xl bg-secondary/30 border border-border/40 flex items-center justify-between group/row hover:bg-secondary/50 transition-colors">
              <div className="min-w-0">
                <p className="text-[9px] uppercase font-black text-muted-foreground/60 tracking-wider">Target Buyer</p>
                <p className="text-xs font-bold truncate">{deal.b1n}</p>
              </div>
              <Button size="icon" variant="ghost" className="h-7 w-7 rounded-lg hover:bg-primary/10 hover:text-primary opacity-0 group-hover/row:opacity-100 transition-all" onClick={e => { e.stopPropagation(); handleCopy(deal.b1p, `bc-${deal.n}`) }}>
                {copiedId === `bc-${deal.n}` ? <CheckCircle2 className="w-3.5 h-3.5" /> : <Phone className="w-3.5 h-3.5" />}
              </Button>
            </div>
          </div>

          <div className="mt-auto flex items-center justify-between pt-3 border-t border-border/40">
            <div className="px-2 py-1 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
              <p className="text-[8px] font-black text-emerald-600/80 dark:text-emerald-400/80 uppercase tracking-widest leading-none mb-0.5">Est. Profit</p>
              <p className="text-sm font-black text-emerald-600 dark:text-emerald-400 font-studio">
                {new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(fee)}
              </p>
            </div>

            {moveDeal && currentColumn && (
              <div className="relative" onClick={e => e.stopPropagation()}>
                <Button
                  size="sm"
                  variant="ghost"
                  className="h-8 text-[10px] font-black uppercase tracking-wider px-2 gap-1.5 hover:bg-primary/10 hover:text-primary rounded-lg"
                  onClick={() => setStageOpen(v => !v)}
                >
                  <div className={`w-1.5 h-1.5 rounded-full ${COLUMN_COLORS[currentColumn]}`} />
                  Move
                </Button>
                {stageOpen && (
                  <div className="absolute bottom-full right-0 mb-2 z-[100] glass-panel rounded-xl overflow-hidden min-w-[180px] animate-in fade-in zoom-in-95 duration-200">
                    <div className="p-1.5 space-y-0.5">
                      {COLUMNS.map(col => (
                        <button
                          key={col}
                          disabled={col === currentColumn}
                          className={`w-full text-left px-3 py-2 rounded-lg text-[11px] font-bold transition-all flex items-center justify-between group ${
                            col === currentColumn 
                            ? 'bg-primary/10 text-primary cursor-default' 
                            : 'hover:bg-accent text-muted-foreground hover:text-foreground'
                          }`}
                          onClick={() => { moveDeal(deal, currentColumn, col); setStageOpen(false) }}
                        >
                          <div className="flex items-center gap-2">
                            <div className={`w-2 h-2 rounded-full ${COLUMN_COLORS[col]}`} />
                            {col}
                          </div>
                          {col === currentColumn && <CheckCircle2 className="w-3 h-3" />}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

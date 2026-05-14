import React, { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Search, MapPin, Building2, Phone, DollarSign, LayoutDashboard, CheckCircle2, ChevronRight, FileText, Globe, AlertTriangle, Columns, LayoutGrid, Menu, X, Sun, Moon, ChevronDown, Share2, Link2, Bell, BellOff, StickyNote } from 'lucide-react'
import { useSwipeable } from 'react-swipeable'
import { DealNotes } from './DealNotes'
import { generateBuyerDealSheet, copyShareableLink } from './ShareSheet'
import { DragDropContext, Droppable, Draggable, DropResult } from '@hello-pangea/dnd'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import jsPDF from 'jspdf'
import L from 'leaflet'

// Fix Leaflet icons
import iconUrl from 'leaflet/dist/images/marker-icon.png'
import iconShadow from 'leaflet/dist/images/marker-shadow.png'
let DefaultIcon = L.icon({ iconUrl, shadowUrl: iconShadow, iconAnchor: [12, 41] })
L.Marker.prototype.options.icon = DefaultIcon

import { deals } from './data'
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

export default function App() {
  const [search, setSearch] = useState('')
  const [selectedDeal, setSelectedDeal] = useState<any>(null)
  const [copiedId, setCopiedId] = useState<string | null>(null)
  const [filterMode, setFilterMode] = useState<'all' | 'vacant' | 'institutional'>('all')
  const [viewMode, setViewMode] = useState<'grid' | 'kanban'>('kanban')
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
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
    if (saved) return JSON.parse(saved)
    return { 'New Lead': deals, 'Contacted': [], 'Negotiating': [], 'Under Contract': [], 'Closed': [] }
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



  const generatePSA = (deal: any) => {
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
    <div className="flex h-[100dvh] bg-background text-foreground dark overflow-hidden">

      {/* Desktop Sidebar */}
      <aside className="hidden md:flex w-72 flex-col glass-panel border-r border-white/5 z-20 shrink-0">
        <div className="p-6">
          <h1 className="text-2xl font-bold tracking-tight text-gradient flex items-center gap-2">
            <LayoutDashboard className="w-6 h-6 text-primary" />
            Land CRM
          </h1>
          <p className="text-sm text-muted-foreground mt-2">Institutional Wholesaling</p>
        </div>
        <div className="px-4 py-2">
          <div className="space-y-1">
            <Button variant={filterMode === 'all' ? 'secondary' : 'ghost'} className="w-full justify-start" onClick={() => setFilterMode('all')}>
              <LayoutDashboard className="w-4 h-4 mr-2" /> All Deals ({deals.length})
            </Button>
            <Button variant={filterMode === 'vacant' ? 'secondary' : 'ghost'} className="w-full justify-start" onClick={() => setFilterMode('vacant')}>
              <MapPin className="w-4 h-4 mr-2" /> Prime Vacant Land
            </Button>
            <Button variant={filterMode === 'institutional' ? 'secondary' : 'ghost'} className="w-full justify-start" onClick={() => setFilterMode('institutional')}>
              <Building2 className="w-4 h-4 mr-2" /> Institutional Target
            </Button>
          </div>
        </div>
        <div className="mt-auto p-6 space-y-4">
          <div className="p-4 rounded-xl bg-gradient-to-br from-primary/20 to-emerald-500/20 border border-white/10 relative overflow-hidden">
            <div className="absolute top-0 right-0 p-4 opacity-10"><DollarSign className="w-24 h-24" /></div>
            <p className="text-xs font-semibold uppercase tracking-wider text-primary/80 mb-1 relative z-10">Total Pipeline Value</p>
            <p className="text-2xl font-bold text-white relative z-10">{formatMoney(deals.reduce((a,d)=>a+d.lv,0))}</p>
          </div>
        </div>
      </aside>

      {/* Mobile Slide-down Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden fixed inset-0 z-50 bg-black/70 backdrop-blur-sm" onClick={() => setMobileMenuOpen(false)}>
          <div className="absolute bottom-16 left-0 right-0 glass-panel border-t border-white/10 p-6 space-y-3" onClick={e => e.stopPropagation()}>
            <div className="p-3 rounded-xl bg-gradient-to-br from-primary/20 to-emerald-500/20 border border-white/10 mb-4">
              <p className="text-xs font-bold uppercase tracking-wider text-primary/80 mb-1">Pipeline Value</p>
              <p className="text-2xl font-black text-white">{formatMoney(deals.reduce((a,d)=>a+d.lv,0))}</p>
            </div>
            <Button variant={filterMode === 'all' ? 'secondary' : 'ghost'} className="w-full justify-start" onClick={() => { setFilterMode('all'); setMobileMenuOpen(false) }}>
              <LayoutDashboard className="w-4 h-4 mr-2" /> All Deals ({deals.length})
            </Button>
            <Button variant={filterMode === 'vacant' ? 'secondary' : 'ghost'} className="w-full justify-start" onClick={() => { setFilterMode('vacant'); setMobileMenuOpen(false) }}>
              <MapPin className="w-4 h-4 mr-2" /> Prime Vacant Land
            </Button>
            <Button variant={filterMode === 'institutional' ? 'secondary' : 'ghost'} className="w-full justify-start" onClick={() => { setFilterMode('institutional'); setMobileMenuOpen(false) }}>
              <Building2 className="w-4 h-4 mr-2" /> Institutional Target
            </Button>
          </div>
        </div>
      )}

      {/* Main Content */}
      <main className="flex-1 flex flex-col h-full overflow-hidden">

        {/* Topbar */}
        <header className="h-16 md:h-20 px-4 md:px-8 flex items-center justify-between glass-panel border-b border-white/5 z-10 shrink-0 gap-3">
          {/* Mobile menu button */}
          <Button variant="ghost" size="icon" className="md:hidden shrink-0" onClick={() => setMobileMenuOpen(v => !v)}>
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </Button>
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              placeholder="Search deals..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-10 bg-background/50 border-white/10 focus:border-primary/50 transition-colors h-10 w-full rounded-full"
            />
          </div>
          <div className="flex items-center gap-1 bg-black/20 p-1 rounded-lg border border-white/5 shrink-0">
            <Button variant={viewMode === 'kanban' ? 'secondary' : 'ghost'} size="sm" onClick={() => setViewMode('kanban')} className="px-2 md:px-3">
              <Columns className="w-4 h-4" /><span className="hidden md:inline ml-2">Pipeline</span>
            </Button>
            <Button variant={viewMode === 'grid' ? 'secondary' : 'ghost'} size="sm" onClick={() => setViewMode('grid')} className="px-2 md:px-3">
              <LayoutGrid className="w-4 h-4" /><span className="hidden md:inline ml-2">Grid</span>
            </Button>
          </div>
          {/* Theme toggle */}
          <Button variant="ghost" size="icon" className="shrink-0" onClick={() => setTheme(t => t === 'dark' ? 'light' : 'dark')}>
            {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
          </Button>
          {/* Notification bell */}
          <Button variant="ghost" size="icon" className="shrink-0 hidden md:flex" onClick={requestNotifications} title={notifPermission === 'granted' ? 'Notifications on' : 'Enable notifications'}>
            {notifPermission === 'granted' ? <Bell className="w-4 h-4 text-primary" /> : <BellOff className="w-4 h-4" />}
          </Button>
        </header>

        {/* Content Area */}
        <div className="flex-1 overflow-auto bg-black/10">
          {viewMode === 'kanban' ? (
            <DragDropContext onDragEnd={onDragEnd}>
              <div className="flex h-full w-max p-8 gap-6">
                {COLUMNS.map(columnId => (
                  <div key={columnId} className="flex flex-col w-[350px] shrink-0 h-full">
                    <div className="flex items-center justify-between mb-4 px-2">
                      <div className="flex items-center gap-2">
                        <span className={`w-2.5 h-2.5 rounded-full ${COLUMN_COLORS[columnId]}`} />
                        <h3 className="font-bold text-lg">{columnId}</h3>
                      </div>
                      <Badge variant="secondary" className="font-bold">{pipeline[columnId].length}</Badge>
                    </div>
                    <Droppable droppableId={columnId}>
                      {(provided, snapshot) => (
                        <div 
                          ref={provided.innerRef} 
                          {...provided.droppableProps}
                          className={`flex-1 overflow-y-auto rounded-2xl p-3 transition-colors min-h-[200px] ${snapshot.isDraggingOver ? 'bg-primary/5 border border-primary/20' : 'bg-white/[0.02] border border-white/5'}`}
                        >
                          {getFilteredList(pipeline[columnId]).map((deal, index) => (
                            <Draggable key={deal.n} draggableId={deal.n.toString()} index={index}>
                              {(provided, snapshot) => (
                                <div
                                  ref={provided.innerRef}
                                  {...provided.draggableProps}
                                  {...provided.dragHandleProps}
                                  className={`mb-4 ${snapshot.isDragging ? 'rotate-2 scale-105' : ''}`}
                                  onClick={() => setSelectedDeal(deal)}
                                >
                                  <DealCard deal={deal} handleCopy={handleCopy} copiedId={copiedId} riskData={riskData[deal.n]} currentColumn={columnId} moveDeal={moveDeal} onOpen={() => setSelectedDeal(deal)} />
                                </div>
                              )}
                            </Draggable>
                          ))}
                          {provided.placeholder}
                        </div>
                      )}
                    </Droppable>
                  </div>
                ))}
              </div>
            </DragDropContext>
          ) : (
            <div className="p-4 md:p-8">
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 md:gap-6">
                {getFilteredList(deals).map(deal => (
                  <div key={deal.n} onClick={() => setSelectedDeal(deal)}>
                    <DealCard deal={deal} handleCopy={handleCopy} copiedId={copiedId} riskData={riskData[deal.n]} />
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
                        {riskData[selectedDeal.n] && riskData[selectedDeal.n].length > 0 && riskData[selectedDeal.n][0].includes("No") === false && (
                          <Badge className="bg-destructive/20 text-destructive-foreground border-none">
                            <AlertTriangle className="w-3 h-3 mr-1" /> RISK FLAGGED
                          </Badge>
                        )}
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
                        {/* Seller */}
                        <div className="flex items-center justify-between bg-amber-500/10 border border-amber-500/20 p-6 rounded-2xl">
                          <div>
                            <h3 className="text-xl font-bold text-amber-500 flex items-center gap-2 mb-2"><Building2 className="w-5 h-5" /> {selectedDeal.seller}</h3>
                            <div className="flex items-center gap-6 text-amber-500/80">
                              <a href={`tel:${selectedDeal.sph}`} className="flex items-center gap-2 hover:text-amber-400 transition-colors">
                                <Phone className="w-4 h-4" /> {selectedDeal.sph}
                              </a>
                            </div>
                          </div>
                          <Button className="bg-amber-500 hover:bg-amber-600 text-amber-950 font-bold" onClick={() => handleCopy(selectedDeal.sph, 'modal-phone')}>
                            {copiedId === 'modal-phone' ? 'Copied!' : 'Copy Phone'}
                          </Button>
                        </div>
                        <div className="bg-card/50 border border-white/5 rounded-2xl p-6 shadow-inner">
                          <p className="text-lg leading-relaxed text-foreground/90 font-serif whitespace-pre-line">{selectedDeal.ss.replace(/\\n/g, '\n')}</p>
                        </div>
                        
                        {/* Buyer */}
                        <div className="flex items-center justify-between bg-blue-500/10 border border-blue-500/20 p-6 rounded-2xl mt-12">
                          <div>
                            <h3 className="text-xl font-bold text-blue-400 flex items-center gap-2 mb-2"><Building2 className="w-5 h-5" /> {selectedDeal.b1n}</h3>
                            <div className="flex items-center gap-6 text-blue-400/80">
                              <a href={`tel:${selectedDeal.b1p}`} className="flex items-center gap-2 hover:text-blue-300 transition-colors">
                                <Phone className="w-4 h-4" /> {selectedDeal.b1p}
                              </a>
                            </div>
                          </div>
                          <Button className="bg-blue-500 hover:bg-blue-600 text-blue-950 font-bold" onClick={() => handleCopy(selectedDeal.b1p, 'modal-buyer-phone')}>
                            {copiedId === 'modal-buyer-phone' ? 'Copied!' : 'Copy Phone'}
                          </Button>
                        </div>
                        <div className="bg-card/50 border border-white/5 rounded-2xl p-6 shadow-inner">
                          <p className="text-lg leading-relaxed text-foreground/90 font-serif whitespace-pre-line">{selectedDeal.bs.replace(/\\n/g, '\n')}</p>
                        </div>
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
      <Card className="h-full bg-card border-border hover:border-primary/40 transition-all overflow-hidden group flex flex-col cursor-pointer shadow-sm hover:shadow-md">
        <CardHeader className="pb-2 pt-3 px-3">
          <div className="flex justify-between items-start mb-1.5">
            <Badge variant="secondary" className="font-mono text-[10px]">#{deal.n}</Badge>
            <div className="flex gap-1">
              {riskData && riskData.length > 0 && riskData[0].includes("No") === false && (
                <Badge variant="destructive" className="text-[10px] px-1"><AlertTriangle className="w-3 h-3" /></Badge>
              )}
              <Badge variant="outline" className="text-primary text-[10px] px-1">{deal.zn}</Badge>
            </div>
          </div>
          <CardTitle className="text-sm font-bold flex items-center gap-1.5 group-hover:text-primary transition-colors" onClick={onOpen}>
            <MapPin className="w-3.5 h-3.5 text-muted-foreground shrink-0" />
            <span className="truncate">{deal.ac} Acres • {deal.city}</span>
          </CardTitle>
        </CardHeader>

        <CardContent className="pt-0 px-3 pb-3 flex-1 flex flex-col gap-2">
          {/* Seller row */}
          <div className="flex items-center justify-between p-2 rounded-lg bg-amber-500/8 border border-amber-500/15" onClick={e => e.stopPropagation()}>
            <div className="min-w-0 flex-1">
              <p className="text-[9px] uppercase tracking-wider text-amber-600 dark:text-amber-400 font-bold mb-0.5">Seller</p>
              <p className="font-medium text-xs truncate">{deal.seller}</p>
            </div>
            <Button size="icon" variant="ghost" className="h-6 w-6 text-amber-500 hover:bg-amber-500/20 shrink-0" onClick={() => handleCopy(deal.sph, `sc-${deal.n}`)}>
              {copiedId === `sc-${deal.n}` ? <CheckCircle2 className="w-3 h-3" /> : <Phone className="w-3 h-3" />}
            </Button>
          </div>

          {/* Buyer row */}
          <div className="flex items-center justify-between p-2 rounded-lg bg-blue-500/8 border border-blue-500/15" onClick={e => e.stopPropagation()}>
            <div className="min-w-0 flex-1">
              <p className="text-[9px] uppercase tracking-wider text-blue-600 dark:text-blue-400 font-bold mb-0.5">Target Buyer</p>
              <p className="font-medium text-xs truncate">{deal.b1n}</p>
            </div>
            <Button size="icon" variant="ghost" className="h-6 w-6 text-blue-500 hover:bg-blue-500/20 shrink-0" onClick={() => handleCopy(deal.b1p, `bc-${deal.n}`)}>
              {copiedId === `bc-${deal.n}` ? <CheckCircle2 className="w-3 h-3" /> : <Phone className="w-3 h-3" />}
            </Button>
          </div>

          {/* Footer: profit + actions */}
          <div className="flex items-center justify-between mt-auto pt-2 border-t border-border">
            <div>
              <p className="text-[9px] uppercase tracking-wider text-muted-foreground font-bold mb-0.5">Est. Profit</p>
              <p className="text-base font-black text-emerald-600 dark:text-emerald-400">
                {new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(fee)}
              </p>
            </div>
            <div className="flex items-center gap-1.5">
              {/* Mobile stage mover — shown always, easy tap target */}
              {moveDeal && currentColumn && (
                <div className="relative" onClick={e => e.stopPropagation()}>
                  <Button
                    size="sm"
                    variant="outline"
                    className="h-7 text-[10px] px-2 gap-1 font-bold"
                    onClick={() => setStageOpen(v => !v)}
                  >
                    <span className={`w-1.5 h-1.5 rounded-full ${COLUMN_COLORS[currentColumn]}`} />
                    Move
                    <ChevronDown className="w-3 h-3" />
                  </Button>
                  {stageOpen && (
                    <div className="absolute bottom-full right-0 mb-1 z-50 bg-card border border-border rounded-xl shadow-xl overflow-hidden min-w-[160px]">
                      {COLUMNS.filter(c => c !== currentColumn).map(col => (
                        <button
                          key={col}
                          className="w-full text-left px-3 py-2.5 text-xs font-bold hover:bg-accent transition-colors flex items-center gap-2"
                          onClick={() => { moveDeal(deal, currentColumn, col); setStageOpen(false) }}
                        >
                          <span className={`w-2 h-2 rounded-full shrink-0 ${COLUMN_COLORS[col]}`} />
                          {col}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              )}
              <Button size="icon" variant="ghost" className="h-7 w-7" onClick={onOpen}>
                <ChevronRight className="w-4 h-4 text-muted-foreground group-hover:text-primary transition-colors" />
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

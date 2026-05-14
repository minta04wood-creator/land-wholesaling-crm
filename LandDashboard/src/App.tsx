import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Search, MapPin, Building2, User, Phone, DollarSign, LayoutList } from 'lucide-react'

import { deals } from './data'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Button } from '@/components/ui/button'

export default function App() {
  const [search, setSearch] = useState('')
  const [selectedDeal, setSelectedDeal] = useState<any>(null)

  const filteredDeals = deals.filter(d => 
    d.city.toLowerCase().includes(search.toLowerCase()) || 
    d.seller.toLowerCase().includes(search.toLowerCase()) || 
    d.b1n.toLowerCase().includes(search.toLowerCase())
  )

  const formatMoney = (val: number) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(val)

  return (
    <div className="min-h-screen bg-background text-foreground dark">
      {/* Header */}
      <header className="sticky top-0 z-10 backdrop-blur-xl bg-background/80 border-b border-border">
        <div className="container mx-auto px-4 py-4 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="p-2 bg-primary/10 rounded-lg">
              <LayoutList className="w-6 h-6 text-primary" />
            </div>
            <h1 className="text-xl font-bold tracking-tight">Land Pipeline Dashboard</h1>
          </div>
          
          <div className="relative w-full md:w-96">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input 
              placeholder="Search city, seller, or buyer..." 
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-10 bg-muted/50 border-transparent focus:bg-background transition-colors"
            />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <motion.div 
          layout
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
        >
          <AnimatePresence>
            {filteredDeals.map((deal) => {
              const buyPrice = deal.lv * 0.55
              const fee = deal.lv * 0.15

              return (
                <motion.div
                  layout
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  transition={{ duration: 0.2 }}
                  key={deal.n}
                  onClick={() => setSelectedDeal(deal)}
                >
                  <Card className="h-full cursor-pointer hover:border-primary/50 hover:shadow-lg hover:shadow-primary/5 transition-all overflow-hidden group">
                    <CardHeader className="bg-muted/30 pb-4 border-b border-border group-hover:bg-primary/5 transition-colors">
                      <div className="flex justify-between items-start mb-2">
                        <Badge variant="secondary" className="font-mono">Deal #{deal.n}</Badge>
                        <Badge variant="outline" className="border-primary text-primary bg-primary/10">{deal.zn}</Badge>
                      </div>
                      <CardTitle className="text-lg flex items-center gap-2">
                        <MapPin className="w-4 h-4 text-muted-foreground" />
                        {deal.ac} Acres in {deal.city}
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="pt-4 space-y-4">
                      <div className="grid grid-cols-2 gap-2 text-sm">
                        <div className="space-y-1">
                          <p className="text-muted-foreground text-xs uppercase tracking-wider">Seller</p>
                          <p className="font-medium truncate" title={deal.seller}>{deal.seller}</p>
                        </div>
                        <div className="space-y-1">
                          <p className="text-muted-foreground text-xs uppercase tracking-wider">Target Buyer</p>
                          <p className="font-medium truncate" title={deal.b1n}>{deal.b1n}</p>
                        </div>
                      </div>
                      
                      <div className="p-3 bg-muted/50 rounded-lg border border-border">
                        <p className="text-xs text-muted-foreground uppercase tracking-wider mb-1">Target Assignment Fee</p>
                        <p className="text-2xl font-bold text-emerald-500">{formatMoney(fee)}</p>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              )
            })}
          </AnimatePresence>
        </motion.div>
      </main>

      {/* Deal Modal */}
      <Dialog open={!!selectedDeal} onOpenChange={() => setSelectedDeal(null)}>
        <DialogContent className="max-w-4xl max-h-[90vh] p-0 overflow-hidden flex flex-col bg-background/95 backdrop-blur-2xl border-border/50 shadow-2xl">
          {selectedDeal && (
            <>
              <DialogHeader className="p-6 pb-0">
                <div className="flex items-center gap-3 mb-2">
                  <Badge variant="secondary" className="font-mono">Deal #{selectedDeal.n}</Badge>
                  <Badge variant="outline">{selectedDeal.zn}</Badge>
                  <Badge variant="default" className="bg-emerald-500/10 text-emerald-500 hover:bg-emerald-500/20">
                    Est. Fee: {formatMoney(selectedDeal.lv * 0.15)}
                  </Badge>
                </div>
                <DialogTitle className="text-3xl font-bold flex items-center gap-2">
                  {selectedDeal.ac} Acres in {selectedDeal.city}
                </DialogTitle>
                <DialogDescription>
                  Full playbook and scripts for immediate outreach.
                </DialogDescription>
              </DialogHeader>

              <Tabs defaultValue="seller" className="flex-1 flex flex-col min-h-0 mt-6">
                <div className="px-6 border-b border-border">
                  <TabsList className="w-full justify-start rounded-none border-b-0 bg-transparent p-0 h-auto">
                    <TabsTrigger 
                      value="seller" 
                      className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent px-6 py-3 font-semibold"
                    >
                      Seller Script
                    </TabsTrigger>
                    <TabsTrigger 
                      value="buyer"
                      className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent px-6 py-3 font-semibold"
                    >
                      Buyer Pitch
                    </TabsTrigger>
                    <TabsTrigger 
                      value="math"
                      className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary data-[state=active]:bg-transparent px-6 py-3 font-semibold"
                    >
                      Deal Math
                    </TabsTrigger>
                  </TabsList>
                </div>

                <ScrollArea className="flex-1 p-6">
                  <TabsContent value="seller" className="mt-0 space-y-6">
                    <div className="flex items-start justify-between bg-amber-500/10 border border-amber-500/20 p-4 rounded-xl">
                      <div className="space-y-1">
                        <h3 className="font-semibold text-amber-500 flex items-center gap-2">
                          <Building2 className="w-4 h-4" />
                          Target: {selectedDeal.seller}
                        </h3>
                        <p className="text-amber-500/80 flex items-center gap-2">
                          <Phone className="w-4 h-4" />
                          {selectedDeal.sph}
                        </p>
                      </div>
                      <Badge variant="outline" className="border-amber-500/50 text-amber-500">Disposition Dept</Badge>
                    </div>

                    <div className="space-y-4">
                      <h4 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">Call Script</h4>
                      <div className="prose prose-invert max-w-none">
                        {selectedDeal.ss.split('\\n').map((p: string, i: number) => (
                          <p key={i} className="text-lg leading-relaxed text-foreground/90 font-serif border-l-4 border-amber-500/50 pl-4 py-1">{p}</p>
                        ))}
                      </div>
                    </div>

                    <div className="bg-primary/5 border border-primary/20 rounded-xl p-4">
                      <h4 className="text-sm font-semibold text-primary mb-2 flex items-center gap-2">
                        💡 Leverage Point
                      </h4>
                      <p className="text-foreground/80">{selectedDeal.lev}</p>
                    </div>
                  </TabsContent>

                  <TabsContent value="buyer" className="mt-0 space-y-6">
                    <div className="flex items-start justify-between bg-blue-500/10 border border-blue-500/20 p-4 rounded-xl">
                      <div className="space-y-1">
                        <h3 className="font-semibold text-blue-400 flex items-center gap-2">
                          <User className="w-4 h-4" />
                          Target: {selectedDeal.b1n}
                        </h3>
                        <p className="text-blue-400/80 flex items-center gap-2">
                          <Phone className="w-4 h-4" />
                          {selectedDeal.b1p}
                        </p>
                      </div>
                      <Badge variant="outline" className="border-blue-500/50 text-blue-400">Institutional Buyer</Badge>
                    </div>

                    <div className="space-y-4">
                      <h4 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">Email / Call Pitch</h4>
                      <div className="prose prose-invert max-w-none">
                        {selectedDeal.bs.split('\\n').map((p: string, i: number) => (
                          <p key={i} className="text-lg leading-relaxed text-foreground/90 font-serif border-l-4 border-blue-500/50 pl-4 py-1">{p}</p>
                        ))}
                      </div>
                    </div>
                  </TabsContent>

                  <TabsContent value="math" className="mt-0">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <Card className="bg-muted/30">
                        <CardHeader className="pb-2">
                          <CardDescription>Estimated Land Value</CardDescription>
                          <CardTitle className="text-3xl">{formatMoney(selectedDeal.lv)}</CardTitle>
                        </CardHeader>
                      </Card>
                      <Card className="bg-muted/30">
                        <CardHeader className="pb-2">
                          <CardDescription>Max Allowable Offer (55%)</CardDescription>
                          <CardTitle className="text-3xl text-amber-500">{formatMoney(selectedDeal.lv * 0.55)}</CardTitle>
                        </CardHeader>
                      </Card>
                      <Card className="bg-emerald-500/10 border-emerald-500/20 md:col-span-2">
                        <CardHeader className="pb-2">
                          <CardDescription className="text-emerald-500/80">Target Assignment Fee</CardDescription>
                          <CardTitle className="text-4xl text-emerald-500">{formatMoney(selectedDeal.lv * 0.15)}</CardTitle>
                        </CardHeader>
                        <CardContent>
                          <p className="text-emerald-500/70 text-sm">Target Buyer Price: {formatMoney((selectedDeal.lv * 0.55) + (selectedDeal.lv * 0.15))} (Still ~30% below market)</p>
                        </CardContent>
                      </Card>
                    </div>
                  </TabsContent>
                </ScrollArea>
              </Tabs>
            </>
          )}
        </DialogContent>
      </Dialog>
    </div>
  )
}

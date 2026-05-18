import React, { useMemo } from 'react'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Fix Leaflet icons
import iconUrl from 'leaflet/dist/images/marker-icon.png'
import iconShadow from 'leaflet/dist/images/marker-shadow.png'

let DefaultIcon = L.icon({
  iconUrl,
  shadowUrl: iconShadow,
  iconAnchor: [12, 41]
})
L.Marker.prototype.options.icon = DefaultIcon

interface MapViewProps {
  deals: any[]
  onSelectDeal: (deal: any) => void
}

// Gwinnett County approximate center
const CENTER: [number, number] = [33.9526, -84.0077]

// Simple hash function to generate consistent pseudo-random coordinates
const hashString = (str: string) => {
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    hash = (hash << 5) - hash + str.charCodeAt(i)
    hash |= 0 // Convert to 32bit integer
  }
  return hash
}

export default function MapView({ deals, onSelectDeal }: MapViewProps) {
  // Generate consistent coordinates for deals based on their ID or address
  const markers = useMemo(() => {
    return deals.map(deal => {
      // Use existing lat/lng if available, otherwise generate a consistent pseudo-random offset from center
      const hash = hashString(`${deal.n}-${deal.addr}`)
      
      // Seed between -0.15 and +0.15 degrees (~10 miles)
      const latOffset = ((hash % 1000) / 1000) * 0.3 - 0.15
      const lngOffset = (((hash >> 4) % 1000) / 1000) * 0.3 - 0.15
      
      const position: [number, number] = deal.lat && deal.lng 
        ? [deal.lat, deal.lng] 
        : [CENTER[0] + latOffset, CENTER[1] + lngOffset]

      return {
        ...deal,
        position
      }
    })
  }, [deals])

  return (
    <div className="w-full h-full p-4 md:p-8 flex flex-col">
      <div className="mb-4">
        <h2 className="text-2xl font-black font-studio">GIS Map View</h2>
        <p className="text-sm text-muted-foreground">Geographic distribution of your pipeline across Gwinnett County.</p>
      </div>
      
      <div className="flex-1 rounded-2xl overflow-hidden border border-border/50 shadow-xl relative z-0">
        <MapContainer 
          center={CENTER} 
          zoom={11} 
          style={{ height: '100%', width: '100%', zIndex: 0 }}
        >
          {/* Using a sleek, modern tile layer instead of default OSM */}
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>'
            url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
          />
          
          {markers.map(deal => (
            <Marker key={deal.n} position={deal.position}>
              <Popup className="premium-map-popup">
                <div className="p-1 min-w-[200px]">
                  <p className="text-[10px] font-bold text-muted-foreground mb-1 uppercase tracking-wider">#{deal.n} &bull; {deal.zn}</p>
                  <p className="font-bold text-base leading-tight mb-2">{deal.addr}, {deal.city}</p>
                  
                  <div className="space-y-1.5 mb-3">
                    <div className="flex justify-between text-xs">
                      <span className="text-muted-foreground">Acreage:</span>
                      <span className="font-bold">{deal.ac} ac</span>
                    </div>
                    <div className="flex justify-between text-xs">
                      <span className="text-muted-foreground">Est. Profit:</span>
                      <span className="font-bold text-emerald-600">${(deal.lv * 0.15).toLocaleString(undefined, { maximumFractionDigits: 0 })}</span>
                    </div>
                  </div>
                  
                  <button 
                    onClick={() => onSelectDeal(deal)}
                    className="w-full py-1.5 bg-primary text-primary-foreground text-xs font-bold rounded-lg hover:bg-primary/90 transition-colors"
                  >
                    View Deal Details
                  </button>
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  )
}

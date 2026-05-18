const fmt = (val: number) =>
  new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(val)

export async function generateBuyerDealSheet(deal: any) {
  const { default: jsPDF } = await import('jspdf')
  const doc = new jsPDF()
  const pageW = doc.internal.pageSize.getWidth()

  // Header bar
  doc.setFillColor(14, 16, 32)
  doc.rect(0, 0, pageW, 40, 'F')

  doc.setTextColor(255, 255, 255)
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(20)
  doc.text('INVESTMENT OPPORTUNITY', pageW / 2, 18, { align: 'center' })
  doc.setFontSize(11)
  doc.setFont('helvetica', 'normal')
  doc.setTextColor(160, 160, 200)
  doc.text('Brought to you by Institutional Land Acquisitions LLC', pageW / 2, 30, { align: 'center' })

  // Accent line
  doc.setDrawColor(120, 100, 230)
  doc.setLineWidth(1.5)
  doc.line(20, 44, pageW - 20, 44)

  // Property headline
  doc.setTextColor(20, 20, 40)
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(22)
  doc.text(`${deal.ac} Acre ${deal.zn} Parcel`, 20, 60)
  doc.setFontSize(13)
  doc.setFont('helvetica', 'normal')
  doc.setTextColor(80, 80, 100)
  doc.text(`${deal.city}, Gwinnett County, GA ${deal.zp}`, 20, 70)

  // Key numbers box
  const boxY = 78
  doc.setFillColor(245, 244, 255)
  doc.roundedRect(20, boxY, pageW - 40, 40, 4, 4, 'F')
  doc.setDrawColor(180, 170, 240)
  doc.setLineWidth(0.5)
  doc.roundedRect(20, boxY, pageW - 40, 40, 4, 4, 'S')

  const col = (pageW - 40) / 3
  const numberItems = [
    { label: 'Market Value', value: fmt(deal.lv), color: [20, 20, 40] },
    { label: 'Asking Price (55%)', value: fmt(deal.lv * 0.55), color: [160, 120, 20] },
    { label: 'Investor Profit (15%)', value: fmt(deal.lv * 0.15), color: [20, 130, 70] },
  ]

  numberItems.forEach((item, i) => {
    const x = 20 + col * i + col / 2
    doc.setFontSize(8)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(100, 100, 130)
    doc.text(item.label.toUpperCase(), x, boxY + 12, { align: 'center' })
    doc.setFontSize(15)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(...(item.color as [number, number, number]))
    doc.text(item.value, x, boxY + 28, { align: 'center' })
  })

  // Property details section
  const detY = 130
  doc.setTextColor(20, 20, 40)
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(11)
  doc.text('PROPERTY DETAILS', 20, detY)
  doc.setDrawColor(120, 100, 230)
  doc.setLineWidth(0.8)
  doc.line(20, detY + 3, 80, detY + 3)

  const details = [
    ['Parcel ID', deal.n.toString()],
    ['Address', `${deal.addr}, ${deal.city}, GA ${deal.zp}`],
    ['Acreage', `${deal.ac} Acres`],
    ['Zoning', deal.zn],
    ['County', 'Gwinnett County, Georgia'],
  ]

  doc.setFontSize(10)
  details.forEach(([label, val], i) => {
    const y = detY + 14 + i * 12
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(80, 80, 110)
    doc.text(`${label}:`, 20, y)
    doc.setFont('helvetica', 'normal')
    doc.setTextColor(20, 20, 40)
    doc.text(val, 65, y)
  })

  // Why this deal section
  const whyY = 200
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(11)
  doc.setTextColor(20, 20, 40)
  doc.text('WHY THIS DEAL', 20, whyY)
  doc.setDrawColor(120, 100, 230)
  doc.line(20, whyY + 3, 70, whyY + 3)

  const bullets = [
    'Off-market opportunity — not listed on MLS or LoopNet',
    'Motivated seller — flexible on terms and closing timeline',
    'High-growth corridor — Gwinnett County development pressure',
    'Assignment-friendly — clear title with no known encumbrances',
    'Assignable contract available — close in 30 days or less',
  ]

  doc.setFont('helvetica', 'normal')
  doc.setFontSize(10)
  doc.setTextColor(40, 40, 60)
  bullets.forEach((b, i) => {
    doc.text(`• ${b}`, 24, whyY + 14 + i * 10)
  })

  // CTA / Contact
  const ctaY = 265
  doc.setFillColor(14, 16, 32)
  doc.rect(0, ctaY, pageW, 30, 'F')
  doc.setTextColor(255, 255, 255)
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(11)
  doc.text('Ready to assign? Call or email us to lock in this deal.', pageW / 2, ctaY + 12, { align: 'center' })
  doc.setFontSize(9)
  doc.setFont('helvetica', 'normal')
  doc.setTextColor(180, 180, 220)
  doc.text('Institutional Land Acquisitions LLC  |  Gwinnett County, GA  |  Off-Market Specialists', pageW / 2, ctaY + 22, { align: 'center' })

  // Disclaimer
  doc.setFontSize(7)
  doc.setTextColor(150, 150, 160)
  doc.text('This document is for informational purposes only. All figures are estimates. Buyer to perform own due diligence.', pageW / 2, 297, { align: 'center' })

  doc.save(`DealSheet_${deal.n}_${deal.city.replace(/ /g, '_')}.pdf`)
}

export function copyShareableLink(deal: any) {
  const url = `${window.location.origin}?deal=${deal.n}`
  navigator.clipboard.writeText(url)
  return url
}

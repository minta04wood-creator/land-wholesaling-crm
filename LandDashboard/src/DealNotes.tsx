import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Phone, Mail, MessageSquare, Plus, Trash2, Clock } from 'lucide-react'

type ActivityType = 'call' | 'email' | 'note' | 'text'

interface Activity {
  id: string
  type: ActivityType
  text: string
  timestamp: string
}

const TYPE_CONFIG: Record<ActivityType, { icon: React.ReactNode; label: string; color: string }> = {
  call:  { icon: <Phone className="w-3.5 h-3.5" />,         label: 'Call',  color: 'text-emerald-500 bg-emerald-500/10 border-emerald-500/20' },
  email: { icon: <Mail className="w-3.5 h-3.5" />,          label: 'Email', color: 'text-blue-500 bg-blue-500/10 border-blue-500/20' },
  text:  { icon: <MessageSquare className="w-3.5 h-3.5" />, label: 'Text',  color: 'text-purple-500 bg-purple-500/10 border-purple-500/20' },
  note:  { icon: <Clock className="w-3.5 h-3.5" />,          label: 'Note',  color: 'text-amber-500 bg-amber-500/10 border-amber-500/20' },
}

export function DealNotes({ dealId }: { dealId: string }) {
  const key = `deal-notes-${dealId}`
  const [activities, setActivities] = useState<Activity[]>(() => {
    try { return JSON.parse(localStorage.getItem(key) || '[]') } catch { return [] }
  })
  const [text, setText] = useState('')
  const [type, setType] = useState<ActivityType>('call')

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(activities))
  }, [activities, key])

  const addActivity = () => {
    if (!text.trim()) return
    const newItem: Activity = {
      id: Date.now().toString(),
      type,
      text: text.trim(),
      timestamp: new Date().toLocaleString('en-US', { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' }),
    }
    setActivities([newItem, ...activities])
    setText('')
  }

  const deleteActivity = (id: string) => {
    setActivities(activities.filter(a => a.id !== id))
  }

  return (
    <div className="space-y-4">
      {/* Input area */}
      <div className="space-y-3 p-4 rounded-xl border border-border bg-card">
        {/* Type selector */}
        <div className="flex gap-2">
          {(Object.keys(TYPE_CONFIG) as ActivityType[]).map(t => (
            <button
              key={t}
              onClick={() => setType(t)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold border transition-colors ${
                type === t ? TYPE_CONFIG[t].color : 'border-border text-muted-foreground hover:bg-accent'
              }`}
            >
              {TYPE_CONFIG[t].icon}
              {TYPE_CONFIG[t].label}
            </button>
          ))}
        </div>

        <div className="flex gap-2">
          <textarea
            className="flex-1 min-h-[60px] resize-none rounded-lg border border-input bg-background px-3 py-2 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring"
            placeholder={`Log a ${TYPE_CONFIG[type].label.toLowerCase()}...`}
            value={text}
            onChange={e => setText(e.target.value)}
            onKeyDown={e => { if (e.key === 'Enter' && e.metaKey) addActivity() }}
          />
          <Button onClick={addActivity} size="sm" className="self-end gap-1">
            <Plus className="w-4 h-4" /> Add
          </Button>
        </div>
      </div>

      {/* Activity feed */}
      <ScrollArea className="max-h-[280px]">
        {activities.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-32 text-muted-foreground text-sm">
            <Clock className="w-8 h-8 mb-2 opacity-40" />
            <p>No activity yet. Log a call, email, or note.</p>
          </div>
        ) : (
          <div className="space-y-2 pr-2">
            {activities.map(a => (
              <div key={a.id} className="flex gap-3 items-start p-3 rounded-xl border border-border bg-card group">
                <div className={`flex items-center gap-1 px-2 py-1 rounded-md text-[10px] font-black border shrink-0 ${TYPE_CONFIG[a.type].color}`}>
                  {TYPE_CONFIG[a.type].icon}
                  {TYPE_CONFIG[a.type].label}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm leading-snug">{a.text}</p>
                  <p className="text-[10px] text-muted-foreground mt-1">{a.timestamp}</p>
                </div>
                <button
                  onClick={() => deleteActivity(a.id)}
                  className="opacity-0 group-hover:opacity-100 transition-opacity text-muted-foreground hover:text-destructive"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            ))}
          </div>
        )}
      </ScrollArea>
    </div>
  )
}

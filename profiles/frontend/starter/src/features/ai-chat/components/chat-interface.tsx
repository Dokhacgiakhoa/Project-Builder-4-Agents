import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ChatMessage } from '../types';
import { Send, Bot, User } from 'lucide-react';

export const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      sender: 'agent',
      content: 'Xin chào! Tớ là AI Agent Assistant. Frontend Starter Kit đã sẵn sàng kết nối API Contract để nhận tác vụ.',
      timestamp: new Date().toLocaleTimeString(),
    },
  ]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (!input.trim()) return;
    const userMsg: ChatMessage = {
      id: String(Date.now()),
      sender: 'user',
      content: input,
      timestamp: new Date().toLocaleTimeString(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');

    // Mock response demonstration
    setTimeout(() => {
      const agentMsg: ChatMessage = {
        id: String(Date.now() + 1),
        sender: 'agent',
        content: `Đã nhận tín hiệu: "${input}". Logic này được module hóa độc lập tại src/features/ai-chat/.`,
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages((prev) => [...prev, agentMsg]);
    }, 600);
  };

  return (
    <Card title="Interactive AI Agent Sandbox" description="Mẫu giao tiếp phòng vệ (Defensive Chat Component)">
      <div className="h-80 overflow-y-auto space-y-4 p-4 bg-slate-50 border border-slate-200 rounded-lg mb-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex items-start gap-3 ${msg.sender === 'user' ? 'flex-row-reverse' : ''}`}
          >
            <div
              className={`p-2 rounded-full text-white ${
                msg.sender === 'user' ? 'bg-sky-600' : 'bg-slate-700'
              }`}
            >
              {msg.sender === 'user' ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
            </div>
            <div
              className={`max-w-md p-3 rounded-xl text-sm ${
                msg.sender === 'user'
                  ? 'bg-sky-600 text-white rounded-br-none'
                  : 'bg-white border border-slate-200 text-slate-800 rounded-bl-none shadow-sm'
              }`}
            >
              <p>{msg.content}</p>
              <span className="block text-[10px] mt-1 opacity-75 text-right">{msg.timestamp}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Nhập câu lệnh để kiểm thử UI..."
          className="flex-1 px-4 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-sky-500"
        />
        <Button onClick={handleSend} className="flex items-center gap-1.5">
          <Send className="h-4 w-4" /> Gửi
        </Button>
      </div>
    </Card>
  );
};

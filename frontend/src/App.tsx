import React, { useState, useEffect, useRef } from 'react';
import { Send, Settings, User, CheckCircle2, Circle, AlertCircle } from 'lucide-react';
import mockCandidates from '../../backend/data/candidates.json';

const API_BASE = import.meta.env.VITE_API_URL || '/api';

export default function App() {
  const [sessionId] = useState(() => 'sess-' + Math.random().toString(36).substring(2, 9));
  const [started, setStarted] = useState(false);
  const [messages, setMessages] = useState<{role: string, content: string}[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [feedback, setFeedback] = useState<any>(null);
  const [debugMode, setDebugMode] = useState(false);
  const [lastDebug, setLastDebug] = useState<any>(null);
  const [currentScore, setCurrentScore] = useState<number | null>(null);

  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, lastDebug]);

  const startInterview = async () => {
    setLoading(true);
    try {
      const candidate = mockCandidates.candidates[1]; // Alex Turner
      const res = await fetch(`${API_BASE}/interview`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId, candidate })
      });
      const data = await res.json();
      setMessages([{ role: 'interviewer', content: data.reply }]);
      setStarted(true);
    } catch (e) {
      console.error(e);
      alert('Failed to start interview. Ensure backend is running.');
    }
    setLoading(false);
  };

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'candidate', content: userMsg }]);
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/interview`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId, message: userMsg })
      });
      const data = await res.json();
      
      setMessages(prev => [...prev, { role: 'interviewer', content: data.reply }]);
      
      if (data.debug_decision) {
        setLastDebug(data.debug_decision);
      }
      if (data.score !== undefined) {
        setCurrentScore(data.score);
      }
      if (data.done) {
        setFeedback(data.feedback);
      }
    } catch (e) {
      console.error(e);
      alert('Failed to send message.');
    }
    setLoading(false);
  };

  const timelineTopics = [
    { name: "Embeddings", day: 7 },
    { name: "Vector DB", day: 8 },
    { name: "Retrieval", day: 10 },
    { name: "Agents", day: 22 },
    { name: "MCP", day: 23 },
    { name: "Deploy", day: 28 },
    { name: "Capstone", day: 31 }
  ];

  return (
    <div className="flex h-screen bg-gray-950 text-gray-100 font-sans">
      
      {/* LEFT: Timeline */}
      <div className="w-64 border-r border-gray-800 bg-gray-900 p-4 flex flex-col">
        <h2 className="text-xl font-bold mb-6 text-blue-400">Curriculum</h2>
        <div className="flex flex-col space-y-4">
          {timelineTopics.map((t, i) => {
            const isCovered = lastDebug && lastDebug.day >= t.day;
            const isCurrent = lastDebug && lastDebug.day === t.day;
            return (
              <div key={i} className="flex items-center space-x-3">
                {isCovered ? (
                  <CheckCircle2 className="w-5 h-5 text-green-500" />
                ) : isCurrent ? (
                  <AlertCircle className="w-5 h-5 text-blue-500 animate-pulse" />
                ) : (
                  <Circle className="w-5 h-5 text-gray-600" />
                )}
                <span className={isCovered ? "text-gray-300" : isCurrent ? "text-blue-400 font-medium" : "text-gray-600"}>
                  {t.name}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* CENTER: Chat */}
      <div className="flex-1 flex flex-col relative bg-gray-950">
        <div className="h-14 border-b border-gray-800 flex items-center justify-between px-6 bg-gray-900/50">
          <h1 className="font-semibold text-lg">Interview Engine</h1>
          <button onClick={() => setDebugMode(!debugMode)} className={`flex items-center space-x-2 text-sm px-3 py-1.5 rounded-md transition-colors ${debugMode ? 'bg-purple-900/50 text-purple-400' : 'text-gray-400 hover:bg-gray-800'}`}>
            <Settings className="w-4 h-4" />
            <span>Debug Mode</span>
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {!started ? (
            <div className="h-full flex items-center justify-center">
              <button onClick={startInterview} disabled={loading} className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-medium transition-colors shadow-lg shadow-blue-900/20">
                {loading ? 'Initializing...' : 'Start Interview'}
              </button>
            </div>
          ) : (
            <>
              {messages.map((m, i) => (
                <div key={i} className={`flex ${m.role === 'candidate' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-2xl rounded-2xl px-5 py-3 ${m.role === 'candidate' ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-200 border border-gray-700/50'}`}>
                    <p className="whitespace-pre-wrap leading-relaxed">{m.content}</p>
                  </div>
                </div>
              ))}
              
              {debugMode && lastDebug && !feedback && (
                <div className="flex justify-start">
                  <div className="max-w-2xl bg-purple-950/30 border border-purple-800/50 rounded-lg p-4 font-mono text-sm text-purple-300 w-full">
                    <div className="text-purple-400 font-bold mb-2 uppercase text-xs tracking-wider">Decision Engine</div>
                    <div><span className="opacity-70">Topic:</span> {lastDebug.title} (Day {lastDebug.day})</div>
                    <div><span className="opacity-70">Difficulty:</span> {lastDebug.difficulty}</div>
                    <div><span className="opacity-70">Probe:</span> {lastDebug.probe}</div>
                    <div><span className="opacity-70">Reason:</span> {lastDebug.reason}</div>
                  </div>
                </div>
              )}
              {loading && messages.length > 0 && (
                <div className="flex justify-start">
                  <div className="bg-gray-800 rounded-2xl px-5 py-4 flex items-center space-x-2">
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" />
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{animationDelay: '150ms'}} />
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{animationDelay: '300ms'}} />
                  </div>
                </div>
              )}
              <div ref={endRef} />
            </>
          )}
        </div>

        {started && !feedback && (
          <form onSubmit={sendMessage} className="p-4 bg-gray-900 border-t border-gray-800">
            <div className="relative flex items-center">
              <input
                type="text"
                value={input}
                onChange={e => setInput(e.target.value)}
                placeholder="Type your response..."
                className="w-full bg-gray-800 border border-gray-700 text-white rounded-full pl-5 pr-12 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all placeholder-gray-500"
                disabled={loading}
              />
              <button
                type="submit"
                disabled={loading || !input.trim()}
                className="absolute right-2 p-2 bg-blue-600 text-white rounded-full hover:bg-blue-500 disabled:opacity-50 disabled:hover:bg-blue-600 transition-colors"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
          </form>
        )}
      </div>

      {/* RIGHT: Profile & Scorecard */}
      <div className="w-80 border-l border-gray-800 bg-gray-900 p-6 flex flex-col overflow-y-auto">
        <div className="flex items-center space-x-4 mb-8">
          <div className="w-12 h-12 bg-gray-800 rounded-full flex items-center justify-center border border-gray-700">
            <User className="w-6 h-6 text-gray-400" />
          </div>
          <div>
            <h2 className="font-bold text-gray-100">Alex Turner</h2>
            <p className="text-sm text-gray-400">Backend Engineer</p>
          </div>
        </div>

        {!feedback ? (
          <div className="space-y-6">
            <div>
              <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Experience</h3>
              <p className="text-gray-300">5 years</p>
            </div>
            <div>
              <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Education</h3>
              <p className="text-gray-300">B.Tech Computer Science</p>
            </div>
            {currentScore !== null && (
              <div className="pt-4 border-t border-gray-800">
                <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Live Score</h3>
                <div className="flex items-center space-x-2">
                  <div className={`text-3xl font-bold ${currentScore >= 80 ? 'text-green-400' : currentScore >= 60 ? 'text-yellow-400' : 'text-red-400'}`}>
                    {currentScore}%
                  </div>
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="animate-fade-in">
            <h2 className="text-xl font-bold text-blue-400 mb-4">Final Scorecard</h2>
            <p className="text-sm text-gray-300 mb-6 leading-relaxed bg-gray-800/50 p-3 rounded-lg border border-gray-700/50">
              {feedback.summary}
            </p>
            
            <div className="mb-6">
              <h3 className="text-sm font-bold text-green-400 mb-2">Strengths</h3>
              <ul className="space-y-2">
                {feedback.strengths.map((s: string, i: number) => (
                  <li key={i} className="text-sm text-gray-300 flex items-start">
                    <span className="text-green-500 mr-2 mt-0.5">•</span>
                    {s}
                  </li>
                ))}
              </ul>
            </div>

            <div className="mb-6">
              <h3 className="text-sm font-bold text-red-400 mb-2">Gaps</h3>
              <ul className="space-y-2">
                {feedback.gaps.map((g: string, i: number) => (
                  <li key={i} className="text-sm text-gray-300 flex items-start">
                    <span className="text-red-500 mr-2 mt-0.5">•</span>
                    {g}
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="text-sm font-bold text-blue-400 mb-2">Next Steps</h3>
              <ul className="space-y-2">
                {feedback.next.map((n: string, i: number) => (
                  <li key={i} className="text-sm text-gray-300 flex items-start">
                    <span className="text-blue-500 mr-2 mt-0.5">→</span>
                    {n}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>

    </div>
  );
}

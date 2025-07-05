// Dashboard UI - Creative Version import React, { useState } from "react"; import { Card, CardContent } from "@/components/ui/card"; import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"; import { Button } from "@/components/ui/button"; import { Sparkles, CloudUpload, Bot } from "lucide-react"; import { motion } from "framer-motion";

const data = { research: [ { title: "AI Research on Elon Musk", timestamp: "2025-07-05 08:30" }, { title: "Trending AI Tools 2025", timestamp: "2025-07-05 07:00" }, ], uploads: [ { title: "Elon Musk AI Explained", time: "08:45", status: "Success", thumbnail: "🎥" }, { title: "Top 5 AI Startups", time: "07:30", status: "Success", thumbnail: "📊" }, ], };

export default function Dashboard() { const [tab, setTab] = useState("research");

return ( <div className="min-h-screen p-6 text-white" style={{ backgroundColor: "#92C8D1", backgroundImage: "url('https://www.transparenttextures.com/patterns/cubes.png')", }} > <h1 className="text-4xl font-bold mb-4 flex items-center gap-3"> <Sparkles className="text-yellow-200 animate-bounce" /> Creative Dashboard </h1>

<Tabs value={tab} onValueChange={setTab} className="w-full">
    <TabsList className="bg-[#fbd1a2] p-2 rounded-xl">
      <TabsTrigger value="research">🔍 Research Logs</TabsTrigger>
      <TabsTrigger value="uploads">📤 Video Uploads</TabsTrigger>
    </TabsList>

    <TabsContent value="research">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
        {data.research.map((item, i) => (
          <Card key={i} className="bg-white bg-opacity-10 text-white rounded-2xl shadow-lg p-4">
            <CardContent>
              <h2 className="text-xl font-semibold mb-1">{item.title}</h2>
              <p className="text-sm opacity-80">{item.timestamp}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </TabsContent>

    <TabsContent value="uploads">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
        {data.uploads.map((item, i) => (
          <Card key={i} className="bg-white bg-opacity-10 text-white rounded-2xl shadow-lg p-4">
            <CardContent>
              <h2 className="text-xl font-semibold mb-1 flex items-center gap-2">
                {item.thumbnail} {item.title}
              </h2>
              <p className="text-sm">Uploaded at: {item.time}</p>
              <p className="text-sm text-green-300">Status: {item.status}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </TabsContent>
  </Tabs>

  <motion.div
    initial={{ x: -100, opacity: 0 }}
    animate={{ x: 0, opacity: 1 }}
    transition={{ delay: 0.8 }}
    className="absolute bottom-10 right-10"
  >
    <img
      src="https://i.ibb.co/MCFbp7v/ironman-fly.png"
      alt="Ironman Flying"
      className="w-32 h-32 animate-float"
    />
  </motion.div>

  <motion.div
    initial={{ y: 100, opacity: 0 }}
    animate={{ y: 0, opacity: 1 }}
    transition={{ delay: 1 }}
    className="absolute top-10 left-6"
  >
    <img
      src="https://i.ibb.co/FqKFbM8/thor-peek.png"
      alt="Thor Peeking"
      className="w-24 h-24"
    />
  </motion.div>
</div>

); }


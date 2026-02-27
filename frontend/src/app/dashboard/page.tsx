"use client"

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Separator } from "@/components/ui/separator";
import { Video, ImageIcon, Sparkles, Upload, Link as LinkIcon, Download } from "lucide-react";

export default function DashboardPage() {
    const [videoUrl, setVideoUrl] = useState("");
    const [artTheme, setArtTheme] = useState("");
    const [isProcessing, setIsProcessing] = useState(false);
    const [generatedClips, setGeneratedClips] = useState<{ title: string, url: string }[]>([]);
    const [statusMessage, setStatusMessage] = useState("");

    // Backend URL dynamic switch wrapper
    const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080";

    // Art State
    const [generatedArts, setGeneratedArts] = useState<{ title: string, image_url: string, image_prompt: string }[]>([]);
    const [artStatusMessage, setArtStatusMessage] = useState("");

    const handleVideoSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!videoUrl) return;

        setIsProcessing(true);
        setGeneratedClips([]);
        setStatusMessage("Iniciando download e processamento...");

        try {
            const response = await fetch(`${API_URL}/api/v1/videos/cut`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ video_url: videoUrl }),
            });
            const data = await response.json();
            const jobId = data.job_id;

            if (!jobId) throw new Error("Job não criado.");

            // Start Polling
            const pollInterval = setInterval(async () => {
                const statusRes = await fetch(`${API_URL}/api/v1/videos/status/${jobId}`);
                if (!statusRes.ok) return;

                const statusData = await statusRes.json();

                if (statusData.status === "done") {
                    clearInterval(pollInterval);
                    setGeneratedClips(statusData.clips);
                    setStatusMessage("");
                    setIsProcessing(false);
                } else if (statusData.status === "error") {
                    clearInterval(pollInterval);
                    setStatusMessage(`Erro: ${statusData.error}`);
                    setIsProcessing(false);
                } else {
                    setStatusMessage("Processando IA e cortando vídeo... Isso pode levar um minuto.");
                }
            }, 3000);

            setVideoUrl("");
        } catch (error: any) {
            console.error(error);
            setStatusMessage("Erro: " + error.message);
            setIsProcessing(false);
        }
    };

    const handleArtSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!artTheme) return;

        setIsProcessing(true);
        setArtStatusMessage("A IA Criativa está trabalhando no seu post...");
        try {
            const response = await fetch(`${API_URL}/api/v1/art/generate/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ theme: artTheme }),
            });
            const data = await response.json();

            if (data.status === "success") {
                setGeneratedArts((prev) => [
                    { title: data.title, image_url: data.image_url, image_prompt: data.image_prompt },
                    ...prev
                ]);
                setArtStatusMessage("");
            } else {
                console.error("API Error:", data);
                setArtStatusMessage("Erro da API: " + (data.detail || "Falhou ao gerar arte."));
            }
        } catch (error: any) {
            console.error(error);
            setArtStatusMessage("Erro de conexão com o servidor de Inteligência Artificial.");
        } finally {
            setIsProcessing(false);
            setArtTheme("");
        }
    };

    return (
        <div className="space-y-6 max-w-5xl mx-auto">
            <div>
                <h1 className="text-3xl font-bold tracking-tight">Criar Conteúdo</h1>
                <p className="text-muted-foreground mt-2">
                    Gere dezenas de clipes virais ou design de posts com IA.
                </p>
            </div>

            <Tabs defaultValue="video" className="w-full">
                <TabsList className="grid w-full max-w-md grid-cols-2 mb-8 h-12">
                    <TabsTrigger value="video" className="flex items-center gap-2 h-10">
                        <Video className="w-4 h-4" />
                        Clipes (Vídeo)
                    </TabsTrigger>
                    <TabsTrigger value="arts" className="flex items-center gap-2 h-10">
                        <ImageIcon className="w-4 h-4" />
                        Artes (Imagem)
                    </TabsTrigger>
                </TabsList>

                {/* --------- VIDEO TAB --------- */}
                <TabsContent value="video" className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

                        {/* Input Section */}
                        <Card className="col-span-1 border-border/50">
                            <CardHeader>
                                <CardTitle className="text-xl">Importar Vídeo</CardTitle>
                                <CardDescription>
                                    Cole um link do YouTube ou faça upload.
                                </CardDescription>
                            </CardHeader>
                            <CardContent>
                                <form onSubmit={handleVideoSubmit} className="space-y-4">
                                    <div className="space-y-2">
                                        <Label htmlFor="youtube-url">URL do YouTube</Label>
                                        <div className="flex gap-2">
                                            <Input
                                                id="youtube-url"
                                                placeholder="https://youtube.com/watch?v=..."
                                                value={videoUrl}
                                                onChange={(e) => setVideoUrl(e.target.value)}
                                            />
                                        </div>
                                    </div>

                                    <div className="flex items-center justify-center my-4">
                                        <Separator className="w-1/3" />
                                        <span className="text-xs text-muted-foreground mx-4">OU</span>
                                        <Separator className="w-1/3" />
                                    </div>

                                    <div
                                        onClick={() => alert("🔧 O recurso de Upload de arquivos MP4 diretos está chegando na próxima versão.\n\nPor favor, cole um Link Público do YouTube por enquanto para testar o MVP do Opus Clip!")}
                                        className="border-2 border-dashed border-border/50 rounded-lg p-6 flex flex-col items-center justify-center text-center hover:bg-muted/30 cursor-pointer transition-colors"
                                    >
                                        <Upload className="w-8 h-8 text-muted-foreground mb-4" />
                                        <p className="text-sm font-medium">Fazer upload de .MP4</p>
                                        <p className="text-xs text-muted-foreground mt-1 text-balance">
                                            Em Breve
                                        </p>
                                    </div>

                                    <Button
                                        type="submit"
                                        className="w-full"
                                        disabled={(!videoUrl && !isProcessing) || isProcessing}
                                    >
                                        {isProcessing ? "Gerando..." : "Gerar Cortes Virais"}
                                        {!isProcessing && <Sparkles className="w-4 h-4 ml-2" />}
                                    </Button>

                                    {statusMessage && (
                                        <p className="text-sm text-center text-primary font-medium mt-4 animate-pulse">
                                            {statusMessage}
                                        </p>
                                    )}
                                </form>
                            </CardContent>
                        </Card>

                        {/* Results Section */}
                        <Card className="col-span-1 md:col-span-2 border-border/50 bg-muted/20">
                            <CardHeader>
                                <CardTitle>Clipes Gerados</CardTitle>
                                <CardDescription>
                                    Seus cortes prontos para o TikTok / Reels aparecerão aqui.
                                </CardDescription>
                            </CardHeader>
                            <CardContent>
                                {generatedClips.length === 0 ? (
                                    <div className="flex flex-col items-center justify-center h-64 text-center border border-dashed rounded-lg border-border/40">
                                        <Video className="w-10 h-10 text-muted-foreground/50 mb-4" />
                                        <p className="text-muted-foreground">
                                            Nenhum clipe gerado ainda.<br />
                                            Importe um vídeo para começar a mágica.
                                        </p>
                                    </div>
                                ) : (
                                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                        {generatedClips.map((clip, idx) => (
                                            <div key={idx} className="bg-card border rounded-lg overflow-hidden flex flex-col">
                                                <video src={clip.url} controls className="w-full aspect-[9/16] object-cover bg-black" />
                                                <div className="p-3">
                                                    <p className="font-medium text-sm line-clamp-2">{clip.title}</p>
                                                    <a href={clip.url} download className="block mt-3">
                                                        <Button variant="outline" size="sm" className="w-full">
                                                            <Download className="w-4 h-4 mr-2" /> Baixar MP4
                                                        </Button>
                                                    </a>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </CardContent>
                        </Card>

                    </div>
                </TabsContent>

                {/* --------- ARTS TAB --------- */}
                <TabsContent value="arts" className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

                        {/* Input Section */}
                        <Card className="col-span-1 border-border/50">
                            <CardHeader>
                                <CardTitle className="text-xl">Criar Nova Arte</CardTitle>
                                <CardDescription>
                                    Digite o tema e a IA fará o design.
                                </CardDescription>
                            </CardHeader>
                            <CardContent>
                                <form onSubmit={handleArtSubmit} className="space-y-4">
                                    <div className="space-y-2">
                                        <Label htmlFor="theme">Tema do Post</Label>
                                        <Input
                                            id="theme"
                                            placeholder='Ex: "5 Dicas de Vendas"'
                                            value={artTheme}
                                            onChange={(e) => setArtTheme(e.target.value)}
                                        />
                                    </div>

                                    <div className="space-y-2">
                                        <Label htmlFor="style">Estilo Visual</Label>
                                        <select id="style" className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50">
                                            <option>Profissional / Corporativo</option>
                                            <option>Minimalista Escuro</option>
                                            <option>Degradê Vibrante</option>
                                        </select>
                                    </div>

                                    <Button
                                        type="submit"
                                        className="w-full mt-4"
                                        variant="default"
                                        disabled={(!artTheme && !isProcessing) || isProcessing}
                                    >
                                        {isProcessing ? "Gerando Design..." : "Gerar Arte"}
                                        {!isProcessing && <ImageIcon className="w-4 h-4 ml-2" />}
                                    </Button>

                                    {artStatusMessage && (
                                        <p className="text-sm text-center text-primary font-medium mt-4 animate-pulse">
                                            {artStatusMessage}
                                        </p>
                                    )}
                                </form>
                            </CardContent>
                        </Card>

                        {/* Results Section */}
                        <Card className="col-span-1 md:col-span-2 border-border/50 bg-muted/20">
                            <CardHeader>
                                <CardTitle>Artes Geradas</CardTitle>
                                <CardDescription>
                                    Posts e Thumbnails prontas.
                                </CardDescription>
                            </CardHeader>
                            <CardContent>
                                {generatedArts.length === 0 ? (
                                    <div className="flex flex-col items-center justify-center h-64 text-center border border-dashed rounded-lg border-border/40">
                                        <ImageIcon className="w-10 h-10 text-muted-foreground/50 mb-4" />
                                        <p className="text-muted-foreground">
                                            Nenhuma arte gerada ainda.<br />
                                            Digite um tema para criar Designs automaticamente.
                                        </p>
                                    </div>
                                ) : (
                                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                        {generatedArts.map((art, idx) => (
                                            <div key={idx} className="bg-card border rounded-lg overflow-hidden flex flex-col">
                                                <img src={art.image_url} alt={art.title} className="w-full aspect-[9/16] object-cover bg-black" />
                                                <div className="p-3">
                                                    <p className="font-medium text-sm line-clamp-2">{art.title}</p>
                                                    <a href={art.image_url} target="_blank" rel="noreferrer" download className="block mt-3">
                                                        <Button variant="outline" size="sm" className="w-full">
                                                            <Download className="w-4 h-4 mr-2" /> Ampliar / Baixar
                                                        </Button>
                                                    </a>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </CardContent>
                        </Card>

                    </div>
                </TabsContent>
            </Tabs>
        </div>
    );
}

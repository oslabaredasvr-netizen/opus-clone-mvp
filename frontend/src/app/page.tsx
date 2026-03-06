import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight, Video, ImageIcon, CheckCircle } from "lucide-react";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Navbar Simple */}
      <header className="px-6 py-4 flex items-center justify-between border-b border-border/40">
        <div className="flex items-center gap-2 font-bold text-xl">
          <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-primary-foreground">
            OC
          </div>
          OpusClone SaaS
        </div>
        <nav className="flex items-center gap-4">
          <Link href="/login" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
            Login
          </Link>
          <Link href="/login">
            <Button size="sm">Começar Grátis</Button>
          </Link>
        </nav>
      </header>

      {/* Hero Section */}
      <main className="flex-1 flex flex-col items-center justify-center text-center px-6 py-24">
        <div className="inline-flex items-center rounded-full border border-border px-3 py-1 text-sm font-medium mb-8 bg-muted/50">
          <span className="flex h-2 w-2 rounded-full bg-primary mr-2"></span>
          Automação de Conteúdo com IA
        </div>

        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight max-w-4xl mb-6">
          Do Vídeo Longo ao <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-purple-500">Corte Viral</span> em Segundos.
        </h1>

        <p className="text-xl text-muted-foreground max-w-2xl mb-10">
          Nossa IA assiste seu vídeo, encontra os ganchos com maior retenção, adiciona legendas automáticas e exporta pronto para o TikTok e Reels.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 mb-20">
          <Link href="/login">
            <Button size="lg" className="h-12 px-8 text-base w-full sm:w-auto">
              Criar meu primeiro clipe
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </Link>
          <Link href="#features">
            <Button size="lg" variant="outline" className="h-12 px-8 text-base w-full sm:w-auto">
              Ver como funciona
            </Button>
          </Link>
        </div>

        {/* Feature Grid */}
        <div id="features" className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl w-full text-left">
          <div className="p-8 rounded-2xl border border-border/50 bg-card hover:border-primary/50 transition-colors">
            <div className="w-12 h-12 rounded-xl bg-primary/20 flex items-center justify-center mb-6 text-primary">
              <Video className="h-6 w-6" />
            </div>
            <h3 className="text-xl font-bold mb-3">Clipes Automáticos</h3>
            <p className="text-muted-foreground mb-4">
              Cole o link do YouTube. A IA faz o resto: transcrição, cortes virais e legendas dinâmicas hardcoded no centro do vídeo.
            </p>
            <ul className="space-y-2">
              <li className="flex items-center text-sm"><CheckCircle className="h-4 w-4 mr-2 text-primary" /> Modelos otimizados Groq/Llama3</li>
              <li className="flex items-center text-sm"><CheckCircle className="h-4 w-4 mr-2 text-primary" /> Cortes focados em alta retenção</li>
            </ul>
          </div>

          <div className="p-8 rounded-2xl border border-border/50 bg-card hover:border-purple-500/50 transition-colors">
            <div className="w-12 h-12 rounded-xl bg-purple-500/20 flex items-center justify-center mb-6 text-purple-400">
              <ImageIcon className="h-6 w-6" />
            </div>
            <h3 className="text-xl font-bold mb-3">Gerador de Artes</h3>
            <p className="text-muted-foreground mb-4">
              Precisa de uma capa de feed? Digite o tema. A IA gera backgrounds abstratos profissionais e sobrepõe uma tipografia premium.
            </p>
            <ul className="space-y-2">
              <li className="flex items-center text-sm"><CheckCircle className="h-4 w-4 mr-2 text-purple-400" /> Imagens text-to-image de alta qualidade</li>
              <li className="flex items-center text-sm"><CheckCircle className="h-4 w-4 mr-2 text-purple-400" /> Prontas para publicar no Instagram</li>
            </ul>
          </div>
        </div>
      </main>

      <footer className="border-t border-border/40 py-8 text-center text-sm text-muted-foreground">
        <p>© {new Date().getFullYear()} OpusClone SaaS. MVP construído.</p>
      </footer>
    </div>
  );
}

import { Video, ImageIcon, LogOut, LayoutDashboard } from "lucide-react";
import Link from "next/link";

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="flex min-h-screen">
            {/* Sidebar */}
            <aside className="w-64 border-r border-border/40 bg-card hidden md:flex flex-col">
                <div className="p-6 border-b border-border/40 flex items-center gap-2 font-bold text-lg">
                    <div className="w-6 h-6 rounded bg-primary flex items-center justify-center text-[10px] text-primary-foreground">
                        OC
                    </div>
                    OpusClone
                </div>

                <nav className="flex-1 p-4 space-y-2">
                    <Link href="/dashboard" className="flex items-center gap-3 px-3 py-2 rounded-md bg-muted text-foreground transition-colors">
                        <LayoutDashboard className="h-4 w-4" />
                        Visão Geral
                    </Link>
                    <Link href="/dashboard" className="flex items-center gap-3 px-3 py-2 rounded-md text-muted-foreground hover:bg-muted/50 transition-colors">
                        <Video className="h-4 w-4" />
                        Meus Vídeos
                    </Link>
                    <Link href="/dashboard" className="flex items-center gap-3 px-3 py-2 rounded-md text-muted-foreground hover:bg-muted/50 transition-colors">
                        <ImageIcon className="h-4 w-4" />
                        Minhas Artes
                    </Link>
                </nav>

                <div className="p-4 border-t border-border/40">
                    <button className="flex items-center gap-3 px-3 py-2 w-full rounded-md text-muted-foreground hover:bg-red-500/10 hover:text-red-500 transition-colors text-left">
                        <LogOut className="h-4 w-4" />
                        Sair
                    </button>
                </div>
            </aside>

            {/* Main Content Area */}
            <main className="flex-1 flex flex-col h-screen overflow-hidden">
                {/* Mobile Header (Hidden on md) */}
                <header className="md:hidden p-4 border-b border-border/40 flex items-center justify-between bg-card">
                    <div className="font-bold flex items-center gap-2">
                        <div className="w-6 h-6 rounded bg-primary flex items-center justify-center text-[10px] text-primary-foreground">OC</div>
                        OpusClone
                    </div>
                </header>

                <div className="flex-1 overflow-y-auto p-4 md:p-8">
                    {children}
                </div>
            </main>
        </div>
    );
}

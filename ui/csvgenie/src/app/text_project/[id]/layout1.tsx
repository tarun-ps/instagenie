import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/AppSidebarComponent"

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <SidebarProvider>
          <AppSidebar />
          <SidebarTrigger />
          <main className="min-h-screen flex w-full">{children}</main>
        </SidebarProvider>
      </body>
    </html>
  )
}

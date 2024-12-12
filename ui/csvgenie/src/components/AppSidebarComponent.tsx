'use client'
import { Check, Database, Folder, Home, Inbox, Loader2, Mic, Plus, Settings, SidebarIcon, Text } from "lucide-react"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubItem,
  SidebarSeparator,
} from "@/components/ui/sidebar"
import { useState } from "react"
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Button } from "./ui/button"
import '@/styles/theme-sky.css';
import { backendUrl } from "@/lib/utils"
import { useRouter } from "next/navigation"

export function AppSidebar() {
    const [menuChosen, setMenuChosen] = useState<string>("Home");
    const [csvFile, setCsvFile] = useState<File | null>(null);
    const [textInput, setTextInput] = useState<string>("");
    const [audioFile, setAudioFile] = useState<File | null>(null);
    const [newProjectButtonText, setNewProjectButtonText] = useState<string>("Create");
    const router = useRouter();

    const handleCreateProject = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        console.log(csvFile);
        console.log(textInput);
        if (csvFile) {
            setNewProjectButtonText("Processing...");
            const formData = new FormData();
            formData.append('csv_file', csvFile);
            console.log(formData);
            const createProject = async () => {
                const response = await fetch(`${backendUrl}/project`, {
                    method: 'POST',
                    body: formData,
                });
                const data = await response.json();
                console.log(data);
                if(data.id) {
                    router.push(`/project/${data.id}`);
                    setNewProjectButtonText("Done");
                } else {
                    alert("Failed to create project");
                }
            }
            console.log("CSV file being processed");
            createProject();
        } else if (textInput) {
            console.log("Text input entered");
        }
    }
    const handleCreateTextProject = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        console.log(textInput);
        if (textInput) {
            setNewProjectButtonText("Processing...");
            const headers = new Headers();
            headers.append('Content-Type', 'application/json');
            const createTextProject = async () => {
                const response = await fetch(`${backendUrl}/text_project`, {
                    method: 'POST',
                    body: JSON.stringify({ text: textInput }),
                    headers: headers,
                });
                const data = await response.json();
                console.log(data);
                router.push(`/text_project/${data.id}`);
                setNewProjectButtonText("Done");
            }
            console.log("Text input being processed");
            createTextProject();
        } else {
            console.log("No text input entered");
        }
    }
    const handleCreateAudioProject = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        console.log(audioFile);
        if (audioFile) {
            setNewProjectButtonText("Processing...");
            const formData = new FormData();
            formData.append('audio_file', audioFile);
            console.log(formData);
            const createAudioProject = async () => {
                const response = await fetch(`${backendUrl}/audio_project`, {
                    method: 'POST',
                    body: formData,
                });
                const data = await response.json();
                console.log(data);
                router.push(`/audio_project/${data.id}`);
                setNewProjectButtonText("Done");
            }
            console.log("Audio file being processed");
            createAudioProject();
        } else {
            console.log("No audio file entered");
        }
    }
    
    return (
        <Sidebar>
            <SidebarHeader className="w-full">
                <div className="flex items-center w-full">
                    <div className="flex-grow pl-4">
                        <h1 className="text-3xl float-left">instagenie</h1>
                    </div>
                    <div className="flex-grow pr-4">
                        <img className="rounded-md float-left" src="/genie.png" alt="Insta-Genie" height={48} width={48}/>
                    </div>
                </div>
            </SidebarHeader>
            <SidebarContent>
                <SidebarGroup>
                    <SidebarGroupContent>
                        <SidebarMenu>
                            <SidebarMenuItem>
                                <div className="flex items-center gap-2">
                                    <Home/>
                                    <span><a href="/">Home</a></span>
                                </div>
                            </SidebarMenuItem>
                        </SidebarMenu>
                    </SidebarGroupContent>
                </SidebarGroup>
                <SidebarGroup>
                    <SidebarGroupContent>
                        <SidebarMenu>
                            <SidebarMenuItem>
                                <div className="flex items-center gap-2">
                                    <Database/>
                                    <span>Spreadsheet</span>
                                </div>
                                <SidebarMenuSub>
                                    <Dialog>
                                        <SidebarMenuSubItem>
                                            <DialogTrigger asChild>
                                                <div className="flex items-center gap-2">
                                                    <Plus className="text-blue-500 w-4 h-4"/>
                                                    <span>New</span> 
                                                </div>
                                            </DialogTrigger>
                                        </SidebarMenuSubItem>
                                        <DialogContent className="sm:max-w-[425px] card border-radius-4px">
                                        <DialogHeader>
                                        <DialogTitle className="text-black">New Project</DialogTitle>
                                        <DialogDescription className="text-black">
                                            Upload a CSV file to get started.
                                        </DialogDescription>
                                        </DialogHeader>
                                        <form onSubmit={handleCreateProject} className="flex flex-col space-y-4">
                                            <input
                                            type="file"
                                            accept=".csv"
                                            onChange={(e) => {
                                                if (e.target.files && e.target.files[0]) {
                                                setCsvFile(e.target.files[0]);
                                                }
                                            }}
                                            className="border border-gray-300 p-2 rounded"
                                            />
                                            <DialogFooter>
                                                <Button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">{newProjectButtonText}</Button>
                                            </DialogFooter>
                                        </form>
                                    </DialogContent>
                                    </Dialog>
                                    <SidebarMenuSubItem>
                                        <div className="flex items-center gap-2">
                                            <Check className="text-gray-300 w-4 h-4"/>
                                            <a href="/project/completed"><span>Completed</span></a>
                                        </div>
                                    </SidebarMenuSubItem>
                                    <SidebarMenuSubItem>
                                        <div className="flex items-center gap-2">
                                            <Loader2 className="text-gray-300 w-4 h-4"/>
                                            <a href="/project/inprogress"><span>In Progress</span></a>
                                        </div>
                                    </SidebarMenuSubItem>
                                </SidebarMenuSub>
                            </SidebarMenuItem>
                            <SidebarSeparator />
                            <SidebarMenuItem>
                                <div className="flex items-center gap-2">
                                    <Mic/>
                                    <span>Audio Scripts</span>
                                </div>
                                <SidebarMenuSub>
                                    <Dialog>
                                        <SidebarMenuSubItem>
                                            <DialogTrigger asChild>
                                                <div className="flex items-center gap-2">
                                                    <Plus className="text-blue-500 w-4 h-4"/>
                                                    <span>New</span> 
                                                </div>
                                            </DialogTrigger>
                                        </SidebarMenuSubItem>
                                        <DialogContent className="sm:max-w-[425px] card border-radius-4px">
                                        <DialogHeader>
                                        <DialogTitle className="text-black">New Project</DialogTitle>
                                        <DialogDescription className="text-black">
                                            Upload an audio file to get started.
                                        </DialogDescription>
                                        </DialogHeader>
                                        <form onSubmit={handleCreateAudioProject} className="flex flex-col space-y-4">
                                            <input
                                            type="file"
                                            accept=".mp3"
                                            onChange={(e) => {
                                                if (e.target.files && e.target.files[0]) {
                                                setAudioFile(e.target.files[0]);
                                                }
                                            }}
                                            className="border border-gray-300 p-2 rounded"
                                            />
                                            <DialogFooter>
                                                <Button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">{newProjectButtonText}</Button>
                                            </DialogFooter>
                                        </form>
                                    </DialogContent>
                                    </Dialog>
                                    <SidebarMenuSubItem>
                                        <div className="flex items-center gap-2">
                                            <Check className="text-gray-300 w-4 h-4"/>
                                            <a href="/audio_project/completed"><span>Completed</span></a>
                                        </div>
                                    </SidebarMenuSubItem>
                                    <SidebarMenuSubItem>
                                        <div className="flex items-center gap-2">
                                            <Loader2 className="text-gray-300 w-4 h-4"/>
                                            <a href="/audio_project/inprogress"><span>In Progress</span></a>
                                        </div>
                                    </SidebarMenuSubItem>
                                </SidebarMenuSub>
                            </SidebarMenuItem>
                            <SidebarMenuItem>
                                <div className="flex items-center gap-2">
                                    <Text/>
                                    <span>Text Scripts</span>
                                </div>
                                <SidebarMenuSub>
                                    <Dialog>
                                        <SidebarMenuSubItem>
                                            <DialogTrigger asChild>
                                                <div className="flex items-center gap-2">
                                                    <Plus className="text-blue-500 w-4 h-4"/>
                                                    <span>New</span> 
                                                </div>
                                            </DialogTrigger>
                                        </SidebarMenuSubItem>
                                        <DialogContent className="sm:max-w-[425px] card border-radius-4px">
                                        <DialogHeader>
                                        <DialogTitle className="text-black">New Project</DialogTitle>
                                        <DialogDescription className="text-black">
                                           Enter some text to get started.
                                        </DialogDescription>
                                        </DialogHeader>
                                        <form onSubmit={handleCreateTextProject} className="flex flex-col space-y-4">
                                            <textarea
                                            value={textInput}
                                            onChange={(e) => setTextInput(e.target.value)}
                                            rows={5}
                                            className="border border-gray-300 p-2 rounded bg-gray-50 text-gray-900"
                                            placeholder="Enter your text here..."
                                            />
                                            <DialogFooter>
                                                <Button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">{newProjectButtonText}</Button>
                                            </DialogFooter>
                                        </form>
                                    </DialogContent>
                                    </Dialog>
                                    <SidebarMenuSubItem>
                                        <div className="flex items-center gap-2">
                                            <Check className="text-gray-300 w-4 h-4"/>
                                            <a href="/text_project/completed"><span>Completed</span></a>
                                        </div>
                                    </SidebarMenuSubItem>
                                    <SidebarMenuSubItem>
                                        <div className="flex items-center gap-2">
                                            <Loader2 className="text-gray-300 w-4 h-4"/>
                                            <a href="/text_project/inprogress"><span>In Progress</span></a>
                                        </div>
                                    </SidebarMenuSubItem>
                                </SidebarMenuSub>
                            </SidebarMenuItem>
                            <SidebarSeparator />
                            <SidebarMenuItem>
                                <div className="flex items-center gap-2">
                                    <Settings/>
                                    <a href="/settings"><span>Settings</span></a>
                                </div>
                            </SidebarMenuItem>
                        </SidebarMenu>
                    </SidebarGroupContent>
                </SidebarGroup>
            </SidebarContent>
            <SidebarFooter>
                <div className="flex items-center gap-2 pl-4 pb-4">
                    <span>Tarun Sasikumar</span>
                </div>
            </SidebarFooter>
        </Sidebar>
  )
}

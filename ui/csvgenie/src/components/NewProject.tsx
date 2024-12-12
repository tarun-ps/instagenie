'use client'

import { Button } from './ui/button';
import { Card, CardHeader, CardContent, CardTitle, CardDescription } from './ui/card';
import { useState } from 'react';
import { Plus } from "lucide-react";

const NewProject: React.FC = () => {
const [showDialog, setShowDialog] = useState<boolean>(false);
const handleDialogClick = () => {
  setShowDialog(!showDialog);
}
  return (
    <Card className="card mx-auto p-4">
    <CardHeader>
      <div className="flex justify-between items-center">
        <div>
          <CardTitle>Step 1</CardTitle>
          <CardDescription>Pick a question or type your own:</CardDescription>
        </div>
        
      </div>
    </CardHeader>
    <CardContent>
      <Button variant="outline" size="icon" onClick={handleDialogClick}>
          <Plus className="w-4 h-4" />
        </Button>
    </CardContent>
    </Card>
    // {showDialog && (
    // <Dialog>
    //   <DialogTrigger asChild>
    //     <Button variant="outline">New Project</Button>
    //   </DialogTrigger>
    //   <DialogContent>
    //     <DialogHeader>
    //       <DialogTitle>New Project</DialogTitle>
    //       <DialogDescription>
    //         Create a new project to get started.
    //       </DialogDescription>
    //     </DialogHeader>
          
    //     {/* <div className="grid gap-4 py-4">
    //       <div className="grid grid-cols-4 items-center gap-4">
    //         <Label htmlFor="name" className="text-right">
    //           Name
    //         </Label>
    //         <Input id="name" value="Pedro Duarte" className="col-span-3" />
    //       </div>
    //       <div className="grid grid-cols-4 items-center gap-4">
    //         <Label htmlFor="username" className="text-right">
    //           Username
    //         </Label>
    //         <Input id="username" value="@peduarte" className="col-span-3" />
    //       </div>
    //     </div> */}
    //     <DialogFooter>
    //       <Button type="submit">Save changes</Button>
    //     </DialogFooter>
    //   </DialogContent>
    // </Dialog>)}
  );
};

export default NewProject; 
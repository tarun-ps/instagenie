'use client'

import React, { useEffect, useState } from 'react';
import { backendUrl, cdnUrl } from '@/lib/utils';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './ui/card';
import { Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious } from './ui/carousel';
import ColorSwatch from './ColorSwatch';
import { Button } from './ui/button';
import { Separator } from './ui/separator';
import { ChevronLeft, RefreshCcw } from 'lucide-react';
import LoadingComponent from './LoadingComponent';

const AudioProcessingComponent: React.FC<{projectId: string}> = ({projectId}) => {
  const [screenTranscript, setScreenTranscript] = useState<any>(null);
  const [screen, setScreen] = useState<number>(-1);
  const [projectDetails, setProjectDetails] = useState<any>(null);
  const [selectedAssets, setSelectedAssets] = useState<{screen: number, type: string, asset: number, details: any}[]>([]);
  const [totalScreens, setTotalScreens] = useState<number>(-1);
  const [submitDisabled, setSubmitDisabled] = useState<boolean>(true);
  const [loadedScreens, setLoadedScreens] = useState<number[]>([]);
  const pollingInterval = 5000; // 5 seconds
  const [, setProcessingComplete] = useState(false);
  const [projectCreated, setProjectCreated] = useState(false);
  useEffect(() => {
    let interval: NodeJS.Timeout;

    const fetchAssetsStatus = async () => {
      try {
        const response = await fetch(`${backendUrl}/audio_project/${projectId}/assets/status`); // Replace with your endpoint
        if (!response.ok) {
          throw new Error("Failed to fetch assets status");
        }
        const data = await response.json();
        console.log(data);
        setLoadedScreens(data.done_screens);

        // Stop polling if job is complete
        if (data.status === "success") {
          setProcessingComplete(true);
          clearInterval(interval);
        }
      } catch (err: any) {
        console.log(err);
        clearInterval(interval); // Stop polling on error
      }
    };
    fetchAssetsStatus();
    // Start polling
    interval = setInterval(fetchAssetsStatus, pollingInterval);

    // Cleanup interval on component unmount
    return () => clearInterval(interval);
  }, [projectDetails]);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    const fetchProjectCreationStatus = async () => {
      try {
        const response = await fetch(`${backendUrl}/audio_project/${projectId}/status`); // Replace with your endpoint
        if (!response.ok) {
          throw new Error("Failed to fetch project creation status");
        }
        const data = await response.json();
        console.log(data);
        setProjectCreated(data.status === "success");

      // Stop polling if job is complete
      if (data.status === "success") {
        setProcessingComplete(true);
        clearInterval(interval);
      }
    } catch (err: any) {
      console.log(err);
      clearInterval(interval); // Stop polling on error
    }
  };
  fetchProjectCreationStatus();
  // Start polling
  interval = setInterval(fetchProjectCreationStatus, pollingInterval);

  // Cleanup interval on component unmount
  return () => clearInterval(interval);
}, []);

  const handleRefresh = async () => {
    console.log("Refreshing screen assets");
    fetchScreenAssets();
  }
  const fetchScreenAssets = async () => {
    console.log("Fetching screen assets");
    if (!loadedScreens || loadedScreens.length == 0) {
      return;
    }
    if (loadedScreens && loadedScreens.length > 0 && !loadedScreens.includes(screen)) {
      return;
    }
    if (screen == -1 || totalScreens == -1 || screen >= totalScreens) {
      if (screen >= totalScreens && selectedAssets && selectedAssets.length === totalScreens) {
        setSubmitDisabled(false);
      }
      return;
    }
    console.log("Fetching screen assets for screen " + screen);
    const response = await fetch(`${backendUrl}/audio_project/${projectId}/screen/${screen}/assets`);
    console.log(response);
    const data = await response.json();
    console.log(data);
    setScreenTranscript(data);
  }

  useEffect(() => {
    console.log("Screen: " + screen + " Loaded Screens: " + loadedScreens);
    fetchScreenAssets();
  }, [screen, loadedScreens]);

  useEffect(() => {
    console.log("Project ID: " + projectId);
    if (projectId) {
      const fetchProjectDetails = async () => {
        const response = await fetch(`${backendUrl}/audio_project/${projectId}`);
        const data = await response.json();
        let screenToLoad = 0;
        setProjectDetails(data);
        if (data.status === "completed") {
          if (data.data.selected_assets && data.data.selected_assets.assets) {
            screenToLoad = data.data.selected_assets.assets?.length > 0 ? data.data.selected_assets.assets.length - 1 : 0;
          }
          const totalScreens = data.data.script.script_for_timestamp.length;
          console.log("Total screens: " + totalScreens);
          setTotalScreens(totalScreens);
          setSelectedAssets(data.data.selected_assets.assets);
          console.log("Screen to load: " + screenToLoad);
          setScreen(screenToLoad);
        }
      }
      fetchProjectDetails();
    }
  }, [projectCreated]);

  const generateSwatches = (swatches: any) => {
    let tempSwatches: string[] = [];
    for (const colors of Object.values(swatches)) {
      if (Array.isArray(colors)) {
        tempSwatches.push("rgb(" + colors.join(",") + ")");
      }
    }
    return tempSwatches;
  }

  const submitAssets = async () => {
    for (const asset of selectedAssets) {
      if (asset.asset == -1) {
        alert("Screen " + asset.screen + " has no asset selected");
        return;
      }
    }
    const response = await fetch(`${backendUrl}/audio_project/${projectId}/assets`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({assets: selectedAssets}),
    });
    console.log(response);
  }

  const isAssetSelected = (screen: number, type: string, asset: number) => {
    return selectedAssets && selectedAssets.find(a => a.screen == screen && a.type == type && a.asset == asset) != undefined;
  }

  const selectAsset = (screen: number, type: string, asset: number) => {
    console.log("Screen: " + screen + " Type: " + type + " Asset: " + asset);
    const mapping: { [key: string]: string } = {
      "lottie": "lottie",
      "video": "video",
      "image": "image",
    }
    if (!selectedAssets) {
      setSelectedAssets([]);
      const newAssetList: {screen: number, type: string, asset: number, details: any}[] = [];
      const key = mapping[type];
      const assetDetails = screenTranscript.assets[key][asset];
      newAssetList.push({screen: screen, type: type, asset: asset, details: assetDetails});
      setSelectedAssets(newAssetList);
      console.log(newAssetList);
    } else {
      const newAssetList = [...selectedAssets];
      const key = mapping[type];
      const assetDetails = screenTranscript.assets[key][asset];
      if (newAssetList.length > screen && newAssetList[screen]) {
        newAssetList[screen] = {screen: screen, type: type, asset: asset, details: assetDetails};
      } else {
        newAssetList.push({screen: screen, type: type, asset: asset, details: assetDetails});
      }
      setSelectedAssets(newAssetList);
      console.log(newAssetList);
    }
   
    if (screen + 1 >= totalScreens) {
      setSubmitDisabled(false);
    } else {
      setSubmitDisabled(true);
      setScreen(screen + 1);
    }
    
  }

  return (
    <div className="container mx-auto p-4 min-w-[800px]">
      <h1 className="text-2xl font-bold text-center">Audio Processing</h1>
      { (!projectCreated || !projectDetails || !projectDetails.data || !projectDetails.data.transcript) && <div className="flex flex-col items-center">
        <LoadingComponent animation={2}/>
      </div>}
      <br />
      { projectDetails && projectCreated && projectDetails.data &&projectDetails.data.transcript && (
        <Card className="pb-4 mb-4">
          <CardHeader>
          </CardHeader>
          <CardContent>
            {/* add a background iamge that is just a quotation mark */}
            
            <div className="flex flex-col items-left text-stone-100 bg-quote-mark p-4">
              <div className="flex flex-col items-center text-black opacity-100">
                <p> {projectDetails.data.transcript}</p>
              </div>
            </div>
            <Separator className="my-4"/>
            <div className="flex flex-col items-center">
              <audio src={`${cdnUrl}/` + projectDetails.data.audio_url} controls/>
            </div>
          </CardContent>
        </Card>
      )}
      {selectedAssets && selectedAssets.length > 0 && (
        <Card className="pb-4 mb-4">
          <CardHeader className="flex justify-between items-center">
            <CardTitle>Selected Assets</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col items-center">
          <Carousel opts={{align: "start"}} className="w-full max-w-lg">
                <CarouselContent>
                  {selectedAssets.map((asset, index) => (
                    <CarouselItem key={index} className="md:basis-1/2 lg:basis-1/4">
                    <div className="flex items-center justify-center h-full">
                      {asset.type === "lottie" && <video src={`${cdnUrl}/` + asset.details.asset.path} autoPlay loop muted playsInline style={{width: '200px', height: 'auto'}}/>}
                      {asset.type === "image" && <img src={`${cdnUrl}/` + asset.details.asset.path} alt="Stock Imagery" style={{width: '200px', height: 'auto'}}/>}
                      {asset.type === "video" && <video src={`${cdnUrl}/` + asset.details.asset.path} autoPlay loop muted playsInline style={{width: '200px', height: 'auto'}}/>}
                    </div>
                  </CarouselItem>
                  ))}
                </CarouselContent>
                <CarouselPrevious />
                <CarouselNext />
              </Carousel>
          </CardContent>
        </Card>
      )}
      {!screenTranscript && projectDetails && projectDetails.data && projectDetails.data.transcript && <LoadingComponent animation={2}/>}
      {screenTranscript && (
        <Card key={"Screen " + screen + ": [" + screenTranscript.script.start_time + ":" + screenTranscript.script.end_time + "]"}>
          <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              <Button variant="ghost" size="icon" onClick={() => setScreen(screen - 1)}>
                <ChevronLeft className="w-4 h-4" />
              </Button>
            </div>
            <div className="flex flex-col items-center">
              <CardTitle>
                {"Screen " + (screen + 1) + ": [" + screenTranscript.script.start_time + ":" + screenTranscript.script.end_time + "]"}
              </CardTitle>
              <CardDescription>{screenTranscript.script.text}</CardDescription>
            </div>
            <div>
              <Button variant="ghost" size="icon" onClick={() => handleRefresh()}>
                <RefreshCcw className="w-4 h-4" />
              </Button>
            </div>
          </div>
          </CardHeader>
          <CardContent className="flex flex-col items-center">
            {screenTranscript.assets?.lottie && screenTranscript.assets.lottie.length > 0 && (
              <Carousel opts={{align: "start"}} className="w-full max-w-lg pb-4">
                <CarouselContent>
                  {screenTranscript.assets.lottie.map((asset: any, index: number) => (
                    <CarouselItem key={index} className="md:basis-1/2 lg:basis-1/3">
                      <div className="flex items-center justify-center h-full">
                       <Card>
                       <CardContent className="flex aspect-square items-center justify-center p-6">
                       <div className="relative">
                        {asset.asset && <video key={index} src={`${cdnUrl}/` + asset.asset.path} autoPlay loop muted playsInline style={{width: '200px', height: 'auto'}}/>}
                        {!asset.asset && <div className="w-full h-full flex items-center justify-center">No Asset</div>}
                        <div className="mt-2">
                          {asset.asset?.swatches && <ColorSwatch colors={generateSwatches(asset.asset.swatches)} />}
                        </div>
                      </div>
                    </CardContent>
                    <CardFooter>
                      <Button className={isAssetSelected(screen, "lottie", index) ? "w-full bg-sky-500 text-white border-none rounded-md" : "w-full"} onClick={() => selectAsset(screen, "lottie", index)}>Select</Button>
                    </CardFooter>
                    </Card>
                    </div>
                    </CarouselItem>
                  ))}
                </CarouselContent>
                <CarouselPrevious />
                <CarouselNext />
              </Carousel>
            )}
            {screenTranscript.assets?.image && screenTranscript.assets.image.length > 0 && (
              <Carousel opts={{align: "start"}} className="w-full max-w-lg pb-4">
                <CarouselContent>
                  {screenTranscript.assets.image.map((asset: any, index: number) => (
                    <CarouselItem key={index} className="md:basis-1/2 lg:basis-1/3">  
                      <div className="flex items-center justify-center h-full">
                       <Card>
                       <CardContent className="flex aspect-square items-center justify-center p-6">
                      <div className="relative">
                        <img key={index} src={`${cdnUrl}/` + asset.asset.path} alt="Stock Imagery" style={{width: '200px', height: 'auto'}}/>
                        <div className="mt-2"> 
                          {asset.asset.swatches && <ColorSwatch colors={generateSwatches(asset.asset.swatches)} />}
                        </div>
                      </div>
                      </CardContent>
                      <CardFooter>
                      <Button className={isAssetSelected(screen, "image", index) ? "w-full bg-sky-500 text-white border-none rounded-md" : "w-full"} onClick={() => selectAsset(screen, "image", index)}>Select</Button>
                      </CardFooter>
                      </Card>
                    </div>
                    </CarouselItem>
                  ))}
                </CarouselContent>
                <CarouselPrevious />
                <CarouselNext />
            </Carousel>
            )}
            {screenTranscript.assets?.video && screenTranscript.assets.video.length > 0 && (
              <Carousel opts={{align: "start"}} className="w-full max-w-lg pb-4">
                <CarouselContent>
                  {screenTranscript.assets.video.map((asset: any, index: number) => (
                    <CarouselItem key={index} className="md:basis-1/2 lg:basis-1/3">  
                      <div className="flex items-center justify-center h-full">
                        <Card>
                          <CardContent className="flex aspect-square items-center justify-center p-6">
                            <div className="relative">
                              <video key={index} src={`${cdnUrl}/` + asset.asset.path} autoPlay loop muted playsInline style={{ width: '200px', height: 'auto' }} />
                              <div className="mt-2">
                                {asset.asset.swatches && <ColorSwatch colors={generateSwatches(asset.asset.swatches)} />}
                              </div>
                            </div>
                          </CardContent>
                          <CardFooter>
                            <Button className={isAssetSelected(screen, "video", index) ? "w-full bg-sky-500 text-white border-none rounded-md" : "w-full"} onClick={() => selectAsset(screen, "video", index)}>Select</Button>
                          </CardFooter>
                        </Card>
                      </div>
                    </CarouselItem>
                  ))}
                </CarouselContent>
                <CarouselPrevious />
                <CarouselNext />
            </Carousel>
            )}
          </CardContent>
        </Card>
      )}
      {totalScreens > 0 && !submitDisabled && <Button className="w-full mt-4 bg-sky-500 text-white border-none rounded-md" onClick={submitAssets}>Submit</Button>}
    </div>
  );
};

export default AudioProcessingComponent; 
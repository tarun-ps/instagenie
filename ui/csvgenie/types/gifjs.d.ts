declare module 'gif.js' {
  interface GIFOptions {
    workers?: number;
    quality?: number;
  }

  interface AddFrameOptions {
    delay?: number;
  }

  class GIF {
    constructor(options?: GIFOptions);
    addFrame(image: HTMLImageElement, options?: AddFrameOptions): void;
    on(event: 'finished', callback: (blob: Blob) => void): void;
    render(): void;
  }

  export default GIF;
} 
export type Map = {
    id: number;
    name: string;
    imgWidth?: number;
    imgHeight?: number;
    imgUrl: string; // there may not be an image behind the url so we use the imgWidth and imgHeight to determine if there is one to load
};

export type FullMap = Map & {
    markers: Marker[];
};

export type CreateMarker = {
    id?: number;
    x: number;
    y: number;
    title: string;
    description: string;
    icon: string;
    color: string;
};

export type Marker = {
    id: number;
    x: number;
    y: number;
    title: string;
    description: string;
    icon: string;
    color: string;
};

export const markerTypes = [
    "wheelchair",
    "warning",
    "info",
    "elevator",
    "stairs",
    "default",
    "bus",
    "car",
    "bike",
] as const;
export type MapPinType = (typeof markerTypes)[number];

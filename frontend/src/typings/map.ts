export type Map = {
    id: number;
    name: string;
    imgWidth: number;
    imgHeight: number;
    imgUrl: string;
}

export type FullMap = Map & {
    markers: {
        id: number;
        name: string;
        imgWidth: number;
        imgHeight: number;
        imgUrl: string;
        markers: {
            id: number;
            x: number;
            y: number;
            title: string;
            description: string;
            icon: string;
            color: string;
        }[];
    }
}

export type Marker = {
    id?: number;
    x: number;
    y: number;
    title: string;
    description: string;
    icon: string;
    color: string;
}

export const markerTypes = [
    "wheelchair",
    "warning",
    "info",
    "default"
] as const;
export type MapPinType = typeof markerTypes[number];

import { Icon, type IconOptions } from "leaflet";

const customIconDefaultOptions: Omit<IconOptions, "iconUrl"> = {
    iconSize: [20, 20], // size of the icon
    shadowSize: [0, 0], // size of the shadow
    iconAnchor: [20, 20], // point of the icon which will correspond to marker's location
    shadowAnchor: [0, 0], // the same for the shadow
    popupAnchor: [-10, -15], // point from which the popup should open relative to the iconAnchor
};

const iconMap: Record<string, Icon<IconOptions> | undefined> = {
    default: undefined,
} as const;

export function getLIconFromString(iconStr: string): Icon<IconOptions> | undefined {
    return iconMap[iconStr];
}

import { makeGET } from "@/lib/utils";
import { mapViewsSchema, type MapView } from "@/schema/mapView";

export default async function fetchMap(): Promise<MapView[]> {
    const res = await makeGET<unknown>("http://localhost:8080/maps/");
    return mapViewsSchema.parse(res.data);
}

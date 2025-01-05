import { makeGET } from "~/shared/make-query";
import { mapViewsSchema, type MapView } from "~/shared/mapView";

export default async function fetchMap(): Promise<MapView[]> {
    const res = await makeGET<unknown>("http://localhost:8080/maps/");
    return mapViewsSchema.parse(res.data);
}

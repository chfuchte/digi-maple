import { mapViewsSchema, type MapView } from "~/shared/mapView";
import { usersSchema, type User } from "~/shared/user";

export default async function fetchEverything(): Promise<{
    users: User[];
    maps: MapView[];
}> {
    const res = await $fetch<{
      users: unknown;
      maps: unknown;
    }>("http://localhost:8080/")

    return {
        users: usersSchema.parse(res.users),
        maps: mapViewsSchema.parse(res.maps),
    }
}

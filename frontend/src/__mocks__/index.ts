import type { MapView } from "@/schema/mapView";
import type { User } from "@/schema/user";
import { defineStore } from "pinia";
import { ref } from "vue";

type Mockup = {
    users: User[];
    maps: MapView[];
};

export const useMockupData = defineStore("__mockup_data__", () => {
    const data = ref<Mockup>({
        users: [],
        maps: [],
    });

    return data;
});

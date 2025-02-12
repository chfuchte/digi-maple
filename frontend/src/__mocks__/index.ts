import type { MapView } from "@/schema/mapView";
import type { User } from "@/schema/user";
import { defineStore } from "pinia";
import { ref } from "vue";

type Mockup = {
    users: User[];
    maps: MapView[];
};

export const useMockupData = defineStore("__mockup_data__", () => {
    const current_user_idx = ref<number | null>(null);

    const data = ref<Mockup>({
        users: [
            {
                id: 1,
                email: "test@test.de",
                full_name: "Test User",
            },
        ],
        maps: [],
    });

    const getCurrentUser = () => {
        return data.value.users[current_user_idx.value!];
    };

    const setCurrentUser = (email: string | false) => {
        if (email == false) {
            current_user_idx.value = null;
            return;
        }
        current_user_idx.value = data.value.users.findIndex((user) => user.email === email);
    };

    const registerUser = (user: Omit<User, "id">) => {
        data.value.users.push({
            id: data.value.users.length + 1,
            ...user,
        });
    };

    const addMapView = (map: Omit<MapView, "id">) => {
        data.value.maps.push({
            id: data.value.maps.length + 1,
            ...map,
        });
    };

    return {
        getCurrentUser,
        setCurrentUser,
        registerUser,
        addMapView,
        data,
    };
});

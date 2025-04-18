import { tryCatch } from "@/lib/utils";
import axios from "axios";
import { z } from "zod";

export async function uploadMapImg(file: File, mapId: number): Promise<boolean> {
    const formData = new FormData();
    formData.append("image", file);

    const res = await tryCatch(axios.post(`http://localhost:8080/api/maps/upload/${mapId}`, formData));

    if (res.error) {
        return false;
    }

    return res.data.status === 200;
}

export async function createMap(name: string): Promise<number | null> {
    const res = await tryCatch(axios.post("http://localhost:8080/api/maps", { name }));
    if (res.error) {
        return null;
    }

    if (res.data.status !== 200) {
        return null;
    }

    const data = z.object({
        id: z.number(),
    }).safeParse(res.data.data);

    if (!data.success) {
        return null;
    }

    return data.data.id;
}

export async function getMap(mapId: number): Promise<{
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
} | false> {
    const res = await tryCatch(axios.get(`http://localhost:8080/api/maps/${mapId}`));

    if (res.error) {
        return false;
    }

    if (res.data.status !== 200) {
        return false;
    }

    const data = z.object({
        id: z.number(),
        name: z.string(),
        imgWidth: z.number(),
        imgHeight: z.number(),
        imgUrl: z.string(),
        markers: z.array(z.object({
            id: z.number(),
            x: z.number(),
            y: z.number(),
            title: z.string(),
            description: z.string(),
            icon: z.string(),
            color: z.string(),
        })),
    }).safeParse(res.data.data);

    if (!data.success) {
        return false;
    }

    return data.data;
}

export async function getUserMaps(): Promise<{
    id: number;
    name: string;
    imgWidth: number;
    imgHeight: number;
    imgUrl: string;
}[] | false> {
    const res = await tryCatch(axios.get("http://localhost:8080/api/maps/user"));

    if (res.error) {
        return false;
    }

    if (res.data.status !== 200) {
        return false;
    }

    const data = z.array(z.object({
        id: z.number(),
        name: z.string(),
        imgWidth: z.number(),
        imgHeight: z.number(),
        imgUrl: z.string(),
    })).safeParse(res.data.data);

    if (!data.success) {
        return false;
    }

    return data.data;
}

export async function deleteMap(mapId: number): Promise<boolean> {
    const res = await tryCatch(axios.delete(`http://localhost:8080/api/maps/${mapId}`));

    if (res.error) {
        return false;
    }

    return res.data.status === 200;
}

export async function searchMaps(query: string): Promise<{
    id: number;
    name: string;
    imgWidth: number;
    imgHeight: number;
    imgUrl: string;
}[] | false> {
    const res = await tryCatch(axios.get(`http://localhost:8080/api/maps/search/${query}`));

    if (res.error) {
        return false;
    }

    if (res.data.status !== 200) {
        return false;
    }

    const data = z.array(z.object({
        id: z.number(),
        name: z.string(),
        imgWidth: z.number(),
        imgHeight: z.number(),
        imgUrl: z.string(),
    })).safeParse(res.data.data);

    if (!data.success) {
        return false;
    }

    return data.data;
}

export async function addMarker(
    mapId: number,
    x: number,
    y: number,
    title: string,
    description: string,
    icon: string,
    color: string
): Promise<{
    id: number;
} | false> {
    const res = await tryCatch(axios.post(`http://localhost:8080/api/maps/${mapId}/markers`, {
        x,
        y,
        title,
        description,
        icon,
        color,
    }));

    if (res.error) {
        return false;
    }

    if (res.data.status !== 200) {
        return false;
    }

    const data = z.object({
        id: z.number(),
    }).safeParse(res.data.data);

    if (!data.success) {
        return false;
    }

    return data.data;
}

export async function updateMarker(
    mapId: number,
    markerId: number,
    data: {
        x?: number;
        y?: number;
        title?: string;
        description?: string;
        icon?: string;
        color?: string;
    }
): Promise<boolean> {
    const res = await tryCatch(axios.put(`http://localhost:8080/api/maps/${mapId}/markers/${markerId}`, data));

    if (res.error) {
        return false;
    }

    return res.data.status === 200;
}

export async function deleteMarker(mapId: number, markerId: number): Promise<boolean> {
    const res = await tryCatch(axios.delete(`http://localhost:8080/api/maps/${mapId}/markers/${markerId}`));

    if (res.error) {
        return false;
    }

    return res.data.status === 200;
}

export async function updateMap(mapId: number, name: string): Promise<boolean> {
    const res = await tryCatch(axios.put(`http://localhost:8080/api/maps/${mapId}`, { name }));

    if (res.error) {
        return false;
    }

    return res.data.status === 200;
}

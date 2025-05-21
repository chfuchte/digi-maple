import { fetcher } from "@/lib/fetch";
import { tryCatch } from "@/lib/utils";
import type { FullMap, Map } from "@/typings/map";
import { AxiosError } from "axios";
import { z } from "zod";

export async function apiUploadMapImg(file: File, mapId: number): Promise<boolean> {
    const formData = new FormData();
    formData.append("image", file);

    const res = await tryCatch(fetcher.post(`${import.meta.env.VITE_API_BASE_URL}/api/maps/upload/${mapId}`, formData));

    if (res.error) {
        return false;
    }

    return res.data.status === 200;
}

export async function apiCreateMap(name: string): Promise<number | null> {
    const res = await tryCatch(fetcher.post(`${import.meta.env.VITE_API_BASE_URL}/api/maps`, { name }));
    if (res.error) {
        return null;
    }

    if (res.data.status !== 200) {
        return null;
    }

    const data = z
        .object({
            id: z.number(),
        })
        .safeParse(res.data.data);

    if (!data.success) {
        return null;
    }

    return data.data.id;
}

export async function apiGetMap(mapId: number): Promise<FullMap | false> {
    const res = await tryCatch(fetcher.get(`${import.meta.env.VITE_API_BASE_URL}/api/maps/${mapId}`));

    if (res.error) {
        return false;
    }

    if (res.data.status !== 200) {
        return false;
    }

    const data = z
        .object({
            id: z.number(),
            name: z.string(),
            imgWidth: z.number().optional(),
            imgHeight: z.number().optional(),
            imgUrl: z.string(),
            markers: z.array(
                z.object({
                    id: z.number(),
                    x: z.number(),
                    y: z.number(),
                    title: z.string(),
                    description: z.string(),
                    icon: z.string(),
                    color: z.string(),
                }),
            ),
        })
        .safeParse(res.data.data);

    if (!data.success) {
        return false;
    }

    return data.data;
}

export async function apiGetUserMaps(): Promise<Map[] | false> {
    const res = await tryCatch(fetcher.get(`${import.meta.env.VITE_API_BASE_URL}/api/maps/my`));

    if (res.error) {
        return false;
    }

    if (res.data.status !== 200) {
        return false;
    }

    const data = z
        .array(
            z.object({
                id: z.number(),
                name: z.string(),
                imgWidth: z.number().optional(),
                imgHeight: z.number().optional(),
                imgUrl: z.string(),
            }),
        )
        .safeParse(res.data.data);

    if (!data.success) {
        return false;
    }

    return data.data;
}

export async function apiDeleteMap(mapId: number): Promise<boolean> {
    const res = await tryCatch(fetcher.delete(`${import.meta.env.VITE_API_BASE_URL}/maps/${mapId}`));

    if (res.error) {
        return false;
    }

    return res.data.status === 200;
}

export async function apiSearchMaps(query: string): Promise<Map[] | false> {
    const res = await tryCatch(fetcher.get(`${import.meta.env.VITE_API_BASE_URL}/maps/search?s=${query}`));

    if (res.error) {
        if (res.error instanceof AxiosError) {
            if (res.error.response?.status === 404) {
                return [];
            }
        }
        return false;
    }

    if (res.data.status === 404) {
        return [];
    }

    if (res.data.status !== 200) {
        return false;
    }

    const data = z
        .array(
            z.object({
                id: z.number(),
                name: z.string(),
                imgWidth: z.number().optional(),
                imgHeight: z.number().optional(),
                imgUrl: z.string(),
            }),
        )
        .safeParse(res.data.data);

    if (!data.success) {
        return false;
    }

    return data.data;
}

export async function apiAddMarker(
    mapId: number,
    x: number,
    y: number,
    title: string,
    description: string,
    icon: string,
    color: string,
): Promise<
    | {
          id: number;
      }
    | false
> {
    const res = await tryCatch(
        fetcher.post(`${import.meta.env.VITE_API_BASE_URL}/maps/${mapId}/markers`, {
            x,
            y,
            title,
            description,
            icon,
            color,
        }),
    );

    if (res.error) {
        return false;
    }

    if (res.data.status !== 200) {
        return false;
    }

    const data = z
        .object({
            id: z.number(),
        })
        .safeParse(res.data.data);

    if (!data.success) {
        return false;
    }

    return data.data;
}

export async function apiUpdateMarker(
    mapId: number,
    markerId: number,
    data: {
        x?: number;
        y?: number;
        title?: string;
        description?: string;
        icon?: string;
        color?: string;
    },
): Promise<boolean> {
    const res = await tryCatch(fetcher.patch(`${import.meta.env.VITE_API_BASE_URL}/maps/${mapId}/markers/${markerId}`, data));

    if (res.error) {
        return false;
    }

    return res.data.status === 200;
}

export async function apiDeleteMarker(mapId: number, markerId: number): Promise<boolean> {
    const res = await tryCatch(fetcher.delete(`${import.meta.env.VITE_API_BASE_URL}/maps/${mapId}/markers/${markerId}`));

    if (res.error) {
        return false;
    }

    return res.data.status === 200;
}

export async function apiUpdateMap(mapId: number, name: string): Promise<boolean> {
    const res = await tryCatch(fetcher.patch(`${import.meta.env.VITE_API_BASE_URL}/maps/${mapId}`, { name }));

    if (res.error) {
        return false;
    }

    return res.data.status === 200;
}

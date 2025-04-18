import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export type Result<T, E = Error> = {
    data: T;
    error: null;
} | {
    data: null;
    error: E;
};

export async function tryCatch<T, E = Error>(promise: Promise<T>): Promise<Result<T, E>> {
    try {
        const data = await promise;
        return { data, error: null };
    } catch (error) {
        return { data: null, error: error as E };
    }
}


export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

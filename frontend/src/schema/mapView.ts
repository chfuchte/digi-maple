import { z } from "zod";

export const markerTypes = ["default", "info", "warning", "weelchair"] as const;

const mapViewSchema = z.object({
    id: z.number(),
    name: z.string(),
    author: z.string(),
    imgUrl: z.string().url(),
    imgWidth: z.number(),
    imgHeight: z.number(),
    markers: z.array(
        z.object({
            id: z.string(),
            x: z.number(),
            y: z.number(),
            display: z.object({
                title: z.string(),
                description: z.string(),
                markerType: z.enum(markerTypes),
                color: z.string(),
            }),
        }),
    ),
});

const mapViewsSchema = z.array(mapViewSchema);

type MapView = z.infer<typeof mapViewSchema>;
type MapMarker = MapView["markers"][number];

export { type MapView, type MapMarker, mapViewSchema, mapViewsSchema };

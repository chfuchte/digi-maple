import { z } from "zod";

const mapViewSchema = z.object({
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
                markerType: z.enum(["default", "info", "warning", "weelchair"]),
            }),
        }),
    ),
});

type MapView = z.infer<typeof mapViewSchema>;
type MapMarker = MapView["markers"][number];

export { type MapView, type MapMarker, mapViewSchema };

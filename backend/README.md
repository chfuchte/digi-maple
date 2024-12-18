# DB Layout - 18.12.2024

## `maps` table

| Column Name | Data Type | Unique | Nullable | PK  |
| ----------- | --------- | ------ | -------- | --- |
| id          | SERIAL    | YES    | NO       | YES |
| name        | TEXT      | NO     | NO       | NO  |
| authorId    | TEXT      | NO     | NO       | NO  |
| imgUrl      | TEXT      | YES    | NO       | NO  |
| imgWidth    | INTEGER   | NO     | NO       | NO  |
| imgHeight   | INTEGER   | NO     | NO       | NO  |

## `markers` table

| Column Name | Data Type | Unique | Nullable | PK  |
| ----------- | --------- | ------ | -------- | --- |
| id          | SERIAL    | YES    | NO       | YES |
| mapId       | INTEGER   | NO     | NO       | NO  |
| x           | INTEGER   | NO     | NO       | NO  |
| y           | INTEGER   | NO     | NO       | NO  |
| title       | TEXT      | NO     | NO       | NO  |
| description | TEXT      | NO     | NO       | NO  |
| type        | TEXT      | NO     | NO       | NO  |

`type` can be one of the following values: `default | info | warning | weelchair` // default | info | warning | weelchair |

## `users` table

| Column Name | Data Type | Unique | Nullable | PK  |
| ----------- | --------- | ------ | -------- | --- |
| id          | SERIAL    | YES    | NO       | YES |
| username    | TEXT      | YES    | NO       | NO  |
| email       | TEXT      | YES    | NO       | NO  |
| password    | TEXT      | NO     | NO       | NO  |

# /r/TranscribersOfReddit Dataset

Dataset consists of completed transcriptions of image posts submitted on the /r/TranscribersOfReddit subreddit.

This dataset is incomplete, the script can run for longer if more data is needed.

Transcription may contain information other than the text in the image, see /r/TranscribersOfReddit wiki for more info.

## Data format:

#### `data.csv`:

One image per line
`image post id, post url, image url, image transcription`

#### `images/`:

Image filename uses the `image post id` that corresponds to a line in data.csv. `image post id` is based on the post the image/transcription was taken from.

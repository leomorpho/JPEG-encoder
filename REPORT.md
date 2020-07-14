# Project 2

* TODO: Refactor to have either snakecase or camelcase

## Q1

Q1 is divided into different sub-parts: WAV-related, UI-related and compressor-related.

## Compression ratio

While the compression ratios of LZW are better, it does not show the impact of having to pack the dictionary into the file.

_Create a map of my implementation (classes, modules). Describe the interface of all objects._

| Filename  | Huffman | LZW    | LZW-based Huffman | Huffman-based LZW |
| --------- | ------- | ------ | ----------------- | ----------------- |
| Car horn  | 1.5638  | 5.1213 |                   |                   |
| Explosion | 1.1753  | 3.7733 |                   |                   |
| Fire      | 1.1797  | 4.0152 |                   |                   |
| Leopard   | 1.3856  | 4.5684 |                   |                   |
| Wav8bit   | 1.3462  | 4.6984 |                   |                   |



## Q2

The following steps were implemented:

* Separate RGB into YCbCr
  * Split each layer into 8x8 blocks
  * For every block:
    * DCT
    * Quantize
    * Zigzag entropy coding

The opposite was implemented for decoding. Encoding and decoding were implemented at the same time. This made development easier as my `pytests` were just the opposite of one another. It was surprisingly challenging and fun to perform each step. The DCT was the hardest part and I still do not completely understand the mathematics. I do understand the principles at work, which I reckon is the most important.

### Gaussian Mixture Model

Apply GMM on image before lossy compression.

### Colour transform

The conversion from RGB to YCbCr used values from [this wikipedia reference page](https://en.wikipedia.org/wiki/YCbCr).

### 2D Discrete Cosine Transform

### Quantization

The two chroma layers are quantized more aggressively than the luma layer. The 50% tables were taken from the textbook. The 10% and 90% tables were taken from Wikipedia.

### Huffman encoding

## References

* [Comparative data compression techniques and multi-compression results](https://iopscience.iop.org/article/10.1088/1757-899X/53/1/012081/pdf)
* [Cornell University: JPEG](http://pi.math.cornell.edu/~web6140/TopTenAlgorithms/JPEG.html)
* [The JPEG image code format](https://www.massey.ac.nz/~mjjohnso/notes/59731/presentations/jpeg.pdf)
* [Wikipedia JPEG](https://en.wikipedia.org/wiki/JPEG#Encoding)
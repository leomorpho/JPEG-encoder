# Project 2

* TODO: Refactor to have either snakecase or camelcase

## Q1

Q1 is divided into different sub-parts: WAV-related, UI-related and compressor-related.

## Compression ratio

While the compression ratios of LZW are better, it does not show the impact of having to pack the dictionary into the file.

_Create a map of my implementation (classes, modules). Describe the interface of all objects._

For the compression ratio, the input is translated to a list of short integers. The reason is that the audio files we are reading for this assignment would store [0-255] in a short integer. I therefore calculate the space it would take in regards to that (and not a 4 byte integer or float). To get the length in bytes of the encoded data, I divide the length of it by 8 for 8 bits/byte since the codes would be packed together.

The compression ratio only takes into account the payload of the sound file. The size of the Huffman tree itself is not taken into account as a real file would need to have it stored for later decoding.

| Filename  | Huffman | LZW  |
| --------- | ------- | ---- |
| Car horn  | 1.21    | 4.03 |
| Explosion | 1.18    | 3.72 |
| Fire      | 1.20    | 4.04 |
| Leopard   | 1.32    | 4.20 |

From my research online, Huffman generally compresses at 1.5:1 and LZW at 5:1. My ratios are slightly below these. The sounds used for testing may have more entropy than the average, or else my code may have a bug. I tested my code extensively with an 81% code coverage in `pytests` tests.

## Q2

The following implementation is an attempt at a simplified version of JPEG. It is simplified in that it supports only the BMP file specified within the assignment. It currently does not work perfectly, with the quality of the compressed image being much lower than expected. I was unable to debug this part, as the whole project was massive and took me about 60h.



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

The Huffman tree is not part of the written file. Therefore, the file is not currently portable. To make it portable, the huffman tree will need to be persisted with the file.s

### Experimentation

When I tired running DCT and reverse DCT, these are the results. I was making the mistake of dequantizating after the reverse DCT.

![Screen Shot 2020-07-18 at 12.15.02 PM](REPORT.assets/Screen%20Shot%202020-07-18%20at%2012.15.02%20PM.png)

I think there is (was) a bug at that point, but the results were quite exciting, it's like psychadelic art!

In the next one, I had forgotten to add the difference of the DC coefficients (+128) back in during reverse DCT 

![Screen Shot 2020-07-18 at 12.25.04 PM](REPORT.assets/Screen%20Shot%202020-07-18%20at%2012.25.04%20PM.png)

Still not quite there yet. I am trying to find what I have done wrong. I have commented out the quantization steps. I am expecting to see an almost identical image to the original, since I am only running DCT on it.

![Screen Shot 2020-07-18 at 12.41.13 PM](REPORT.assets/Screen%20Shot%202020-07-18%20at%2012.41.13%20PM.png)

July 15: I tested to see if the previous step was much lighter because I was adding 128 to every pixel twice after DCT, but the pixels are clearly out of the [0, 255] bound now:

![Screen Shot 2020-07-18 at 12.44.28 PM](REPORT.assets/Screen%20Shot%202020-07-18%20at%2012.44.28%20PM.png)

I re-wrote my DCT steps as I am pretty confident my bug is there. I made sure to perform the following in order, and then in reverse for reverse DCT:

* Substract 128 for al values
* DCT for rows
* DCT for columns

July22 : Clearly, there is still something wrong. I do think there is an improvement, as the image is not overexposed anymore. 

![Screen Shot 2020-07-22 at 3.30.12 PM](REPORT.assets/Screen%20Shot%202020-07-22%20at%203.30.12%20PM.png)

I applied only the row DCT and adjusted the reverse DCT to set 0 if values were below zero. Looking better.

![Screen Shot 2020-07-22 at 3.36.05 PM](REPORT.assets/Screen%20Shot%202020-07-22%20at%203.36.05%20PM.png)

Adjusted the previous state to also apply column DCT. It is better than before. However, the quality is much lower. I wonder if that is caused by the naive DCT implementation. Otherwise, there is another bug.

![Screen Shot 2020-07-22 at 3.37.28 PM](REPORT.assets/Screen%20Shot%202020-07-22%20at%203.37.28%20PM.png)

Reapplying quantization for 90% quality yields a result which appears to be much lower than 90% of the original's quality.

![Screen Shot 2020-07-22 at 3.42.17 PM](REPORT.assets/Screen%20Shot%202020-07-22%20at%203.42.17%20PM.png)



### Filesize issues

I wonder if the enormous file size is introduced by utf8 encoding. Looking at the byte array, 2 bytes take the space of 16 bytes. There is therefore an issue with what should be a byte ending up being 8 times as large. Each bit is being encoded as a byte.

I did not think that I would be able to fix this size issue, but after finding out that each bit was encoded as a byte, i figured out how to correct it. I converted each string of binary ("11010010") to an integer, then wrote that integer as a single byte to file. I then read that integer and converted it to a binary string.



## References

* [Comparative data compression techniques and multi-compression results](https://iopscience.iop.org/article/10.1088/1757-899X/53/1/012081/pdf)
* [Cornell University: JPEG](http://pi.math.cornell.edu/~web6140/TopTenAlgorithms/JPEG.html)
* [The JPEG image code format](https://www.massey.ac.nz/~mjjohnso/notes/59731/presentations/jpeg.pdf)
* [Wikipedia JPEG](https://en.wikipedia.org/wiki/JPEG#Encoding)
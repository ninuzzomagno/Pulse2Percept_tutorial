# Visual field
Hello everyone, this is an almost only theoretical tutorial, but don't worry: I don'want to scare anyone with the code I appended to this tutorial. Its task is only to demonstrate how our visual field work, so you don't need to understand it.

## Libraries you will need
1. `matplotlib`
2. `opencv-python`

## How much do you see?
With your eyes, you have a large visual field(VF) which is not equal for vertical and horizontal direction. If you consider only your right eye(RE), your VF covers almost 160° in horizontal and 120° in vertical direction. Using both your eyes you can reach almost 180° along horizontal direction. However, we can percieve the world with maximum resolution only in a tiny spot in the center of our VF, called <b>FOVEA</b>. When we move away from the fovea, our visual acuity drops almost instant. So you have a visual acuity of almost 10/10 in your fovea (if you don't have any visual issue ), but, at almost 60° your acuity drops to 1/60!!

## The blind spot
Actually, in your eye there is a blind spot due to the optical nerve which leave your eye before going to your brain.

You can test its presence in this way:
1) take a white sheet of squared paper
2) draw one blu circle with two grid squareds wide
3) count ten squares to the right from the center of the first circle and then draw another circle using red color
4) close your left eye and focus the other on the left circle.
5) slowly, come closer to the paper sheet while the other circle don't disappeare
6) if you continue to come closer the red circle will reappere

## Pratical test: The Goldmann Map
If you want to know how REALLY you see with only your right eye, then run the python script and you will see the <b>Goldmann map</b>

<b>Some important note</b>: the script will create an image and if you will look at the legend you will see written <b>DVA</b>. DVA means degree of visual angle, it's a unit to measure our visual field. It's very important for the next tutorials. <b>ARGUS II</b> and <b>ALPHA IMS</b> are two different visual prostheses which we will use in the future.
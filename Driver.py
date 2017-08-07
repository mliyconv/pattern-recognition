from preprocessor import Preprocessor
import pytesseract
from PIL import Image

def presentation():
    startSingularFileExperiment("receipt3", "jpg")

    print "Done!"

def experiment():
    # startSingularFileExperiment("doc1", "png", withSkel=True)
    # startSingularFileExperiment("flyer1", "png", scale=1)
    # startSingularFileExperiment("pic1", "jpg", scale=1)
    #
    # startSingularFileExperiment("receipt1", "jpg", withSkel=True)
    # startSingularFileExperiment("receipt2", "jpg", withSkel=True)
    # startSingularFileExperiment("receipt3", "jpg", withSkel=True)
    # startSingularFileExperiment("receipt4", "jpg", withSkel=True)
    # startSingularFileExperiment("receipt5", "jpg", withSkel=True, scale=1)
    #
    # startSingularFileExperiment("scan1", "png", scale=1)
    # startSingularFileExperiment("scan2", "png")

    # startSingularFileExperiment("plate1", "png")

    # startSingularFileExperiment("poster1", "jpg", scale=1)
    # startSingularFileExperiment("poster2", "jpg", scale=1)
    # startSingularFileExperiment("poster3", "jpg", scale=1)

    print "Experiment complete!"

def startSingularFileExperiment(imgName, imgType, withSkel=False, scale=3):
    print "************************************************************"
    Preprocessor.Preprocessor(imgName+"."+imgType, imgName+"."+imgType, withSkel, scale=scale)
    print "Done preprocessing with image: " + imgName

    out = pytesseract.image_to_string(Image.open("output/preprocessed/" + imgName + "." + imgType))
    out2 = pytesseract.image_to_string(Image.open("output/preprocessed/" + imgName + "." + imgType), lang="Merchant+Club+Fake+Open+Anonymous+Arial")

    if(withSkel):
        out3 = pytesseract.image_to_string(Image.open("output/skeleton/"+imgName+"."+imgType))
        out4 = pytesseract.image_to_string(Image.open("output/skeleton/" + imgName + "." + imgType), lang="Merchant+Club+Fake+Open+Anonymous+Arial")
        writeToFile(imgName + "_skel.txt", out3)
        writeToFile(imgName + "_skel.txt", out4, False)

    print "Done classifying with image: " + imgName

    writeToFile(imgName+".txt", out)
    writeToFile(imgName+".txt", out2, False)
    print "Done writing to file with image: " + imgName
    print "************************************************************"

def writeToFile(outPath, content, usingOOB = True):
    if(usingOOB):
        file = open("output/text/oob/"+outPath, "w")
    else:
        file = open("output/text/own/" + outPath, "w")

    file.write(content)
    file.close()


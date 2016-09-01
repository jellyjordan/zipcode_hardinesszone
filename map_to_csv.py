import csv
import matplotlib.path as mpl
import shapefile
import sys

def main():
	if len(sys.argv) != 3:
		print "Error: Invalid Format"
		print "Use: map2txt.py \"shapefilepath\" \"zipcodefilepath\""
		sys.exit()

	#Lists for fine tuning the search.
	notFoundList = []		# Nothing found means the polygon borders are not encompassing the whole map and need to be increased.
	waterFoundList = []		# Water found means the polygon borders overlap and need to be reduced.

	# Open all files for procedure.
	hardinessData = shapefile.Reader(sys.argv[1]).shapeRecords()
	zipCodeFile = open(sys.argv[2], 'rb')
	outputFile = open('output', 'w')

	outputWriter = csv.writer(outputFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
	outputWriter.writerow(["Zip" , "Zone"])

	zipCodes = csv.reader(zipCodeFile)
	next(zipCodes, None)
	for zipEntry in zipCodes:
		zipCode = zipEntry[0]
		zipLat = float(zipEntry[1])
		zipLng = float(zipEntry[2])
		plantZone = "N/A"

		for zoneData in hardinessData:
			polygon = mpl.Path(zoneData.shape.points)
			if polygon.contains_point([zipLng, zipLat], None, 1.1):
				plantZone = zoneData.record[3]
				break

		if(plantZone == "N/A"):
			notFoundList.append([zipCode, zipLat, zipLng])
		elif(plantZone == "Water"):
			waterFoundList.append([zipCode, zipLat, zipLng])
		else:
			outputWriter.writerow([zipCode, plantZone])

		print zipCode

	adjustmentSearch(notFoundList, 1, 0.1, outputWriter, hardinessData)
	adjustmentSearch(waterFoundList, 0.5, -0.1, outputWriter, hardinessData)

	zipCodeFile.close()
	outputFile.close()


# Searches for the missing items in the list by increasing or reducing the size of the border.
def adjustmentSearch(missingItemList, initialVal, adjustmentVal, output, hardinessData):
	threshold = 0
	borderRadius = initialVal + adjustmentVal

	while len(missingItemList) > 0 and threshold < 5:
		print "T:{}".format(threshold)
		print "LEN:{}".format(len(missingItemList))
		updatedMissingList = []
		for missingItem in missingItemList:
			print "Zip:{}".format(missingItem[0])
			print "Lat:{}".format(missingItem[1])
			print "Lng:{}".format(missingItem[2])
			plantZone = "N/A"
			for zoneData in hardinessData:
				polygon = mpl.Path(zoneData.shape.points)
				if polygon.contains_point([missingItem[1], missingItem[2]], None, borderRadius):
					plantZone = zoneData.record[3]
					break
			if(plantZone != "N/A" and plantZone != "Water"):
				outputWriter.writerow([missingItem[0], plantZone])
			else:
				updatedMissingList.append(missingItem)
		missingItemList = updatedMissingList
		threshold += 1
		borderRadius += adjustmentVal


main()

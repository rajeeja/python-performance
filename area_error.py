import matplotlib.pyplot as plt
import uxarray as ux
import time
import wget
import os
import xarray as xr

opfiles = []

def timingFunction(fileSize, quadRule, order):
    fileSizes = {
      #   'ne2048np4_scrip_c20190125.nc': 'homme'
      #   'ne512np4_latlon_c20190125.nc': 'homme'
      'ne256np4_scrip_c20190127.nc': 'homme'
    }

    # URL and place to install files
    url = "https://web.lcrc.anl.gov/public/e3sm/inputdata/share/meshes/mpas/homme/"
    destinationPath = "Files/"

    # Create the destination folder if it doesn't exist
    os.makedirs(destinationPath, exist_ok=True)

    fileName = None

    # Download the file if it doesn't exist already
    for name, size in fileSizes.items():
        if size == fileSize:
            fileName = name
            filePath = os.path.join(destinationPath, fileName)
            if os.path.exists(filePath):
                print(f"File already exists: {filePath}")
            else:
                try:
                    downloadedFile = wget.download(url + fileName, out=destinationPath)
                    print(f"File downloaded successfully: {downloadedFile}")
                    print(f"File size: {size}")
                except Exception as e:
                    print(f"Error while downloading: {e}")
            break
    else:
        print(f"No file found with size: {fileSize}")

    if fileName:
        # Open dataset in UXarray
        mpasRootFilePath = "Files/"
        mpasDatasetFilePath = mpasRootFilePath + fileName

        # open_grid()
        openGridStartTime = time.time()
        
      #   load with xarray to compute actual area
      #   actualArea = xr.open_dataset(mpasDatasetFilePath).grid_area.sum()
      #   print("actual area = ", actualArea)
        actualArea = 12.56637061
        
        mpasGrid = ux.open_grid(mpasDatasetFilePath)
        openGridEndTime = time.time()
        openGridTotalTime = openGridEndTime - openGridStartTime
        print(f"OpenGridTotalTime {openGridTotalTime}")

        # encode_as()
        encodeAsStartTime = time.time()
        mpasEncodedUG = mpasGrid.encode_as("ugrid")
        encodeAsEndTime = time.time()
        encodeAsTotalTime = encodeAsEndTime - encodeAsStartTime
        print(f"encodeAsTotalTime: {encodeAsTotalTime}")

        # computer_face_areas()
        faceAreaCalcStartTime = time.time()
        mpasMeshFaceArea = mpasGrid.compute_face_areas(quadrature_rule=quadRule, order=order)
        print("area = ",mpasMeshFaceArea, "sum = ", mpasMeshFaceArea.sum())
        print("error = ", mpasMeshFaceArea.sum() - actualArea)
        print("error percent = ", (mpasMeshFaceArea.sum() - actualArea)*100.0/actualArea)
        faceAreaCalcEndTime = time.time()
        faceAreaCalcTotalTime = faceAreaCalcEndTime - faceAreaCalcStartTime
        print(f"faceAreaCalcTotalTime {faceAreaCalcTotalTime}")

        # Save timing results to a text file
        resultFileName = f"{fileSize}_{quadRule}_{order}.txt"
        opfiles.append(resultFileName)
        resultFilePath = os.path.join("Results", resultFileName)

        if os.path.exists(resultFilePath):
            # Append only the needed data
            with open(resultFilePath, 'a') as file:
                file.write(f"File Size: {fileSize}\n")
                file.write(f"Quadrature Rule: {quadRule}\n")
                file.write(f"Order: {order}\n")
                file.write(f"Face Area Calculation Time: {faceAreaCalcTotalTime} seconds\n")
                file.write(f"percent error: {(mpasMeshFaceArea.sum() - actualArea)*100.0/actualArea}\n")

        else:
            # Create a new file with all the timing data
            with open(resultFilePath, 'w') as file:
                file.write(f"File Size: {fileSize}\n")
                file.write(f"Quadrature Rule: {quadRule}\n")
                file.write(f"Order: {order}\n")
                file.write(f"Open Grid Time: {openGridTotalTime} seconds\n")
                file.write(f"Encode As Time: {encodeAsTotalTime} seconds\n")
                file.write(f"Face Area Calculation Time: {faceAreaCalcTotalTime} seconds\n")
                file.write(f"percent error: {(mpasMeshFaceArea.sum() - actualArea)*100.0/actualArea}\n")
                print(f"Timing results saved to: {resultFilePath}")

    else:
        print("File not found. Unable to proceed.")


def plotAreaCalculationComparison(files):
    file_sizes_with_numba = []
    run_times_with_numba = []
    file_sizes_without_numba = []
    run_times_without_numba = []
    error_gauss = []

    for file in files:
        filepath = os.path.join("Results", file)

        with open(filepath, 'r') as f:
            lines = f.readlines()

            # Skip files with incorrect format
            if len(lines) < 5:
                print(f"Skipping file: {file} - Incorrect format")
                continue

            try:
                file_size = lines[0].split(":")[1].strip()
                quad_rule = lines[1].split(":")[1].strip()
                order = int(lines[2].split(":")[1].strip())
                run_time = float(lines[5].split(':')[1].strip().split()[0])
                error = float(lines[6].split(':')[1].strip().split()[0])

                if "percent error" in file:
                   error_gauss.append(error)
                   


            except (ValueError, IndexError) as e:
                print(f"Skipping file: {file} - Error: {str(e)}")
                continue

    # Plot both lines on the chart
    fig, ax = plt.subplots()
   #  ax.plot(file_sizes_with_numba, run_times_with_numba, marker='o', linestyle='-', label="With Numba")
    ax.plot(order, error_gauss, marker='o', linestyle='-', label="Gaussian")
    ax.set_xlabel("Order")
    ax.set_ylabel("Percentage Error")
    ax.set_title(f"Error Analysis({quad_rule}, {order})")
    ax.legend()
   #  ax.set_yscale('log')

    plt.show()


# Running tri function in loop
triangular_order=[1,4,8,10,12]
for i in triangular_order:
    timingFunction("homme", "triangular", i)

# Running gaussian 1 to 10 order function in loop
for i in range(10):
    timingFunction("homme", "gaussian", i+1)

timingFunction("homme", "gaussian", 9)

# plotAreaCalculationComparison(opfiles)

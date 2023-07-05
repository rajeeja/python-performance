import matplotlib.pyplot as plt
import uxarray as ux
import time
import wget
import os


def timingFunction(fileSize, quadRule, order):
    fileSizes = {
        'oRRS18to6v3.230424.nc': '11G',
        'WC14to60E2r5.230313.nc': '1G',
        'oEC60to30v3.230424.nc': '595KB',
        'oQU120.230424.nc': '98KB',
        'oQU240wLI.230422.nc': '18KB',
        'oQU480.230422.nc': '4KB',
    }

    # URL and place to install files
    url = "https://web.lcrc.anl.gov/public/e3sm/inputdata/share/meshes/mpas/ocean/"
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
        faceAreaCalcEndTime = time.time()
        faceAreaCalcTotalTime = faceAreaCalcEndTime - faceAreaCalcStartTime
        print(f"faceAreaCalcTotalTime {faceAreaCalcTotalTime}")

        # Save timing results to a text file
        resultFileName = f"{fileSize}_with_out_numba.txt"
        resultFilePath = os.path.join("Results", resultFileName)

        if os.path.exists(resultFilePath):
            # Append only the needed data
            with open(resultFilePath, 'a') as file:
                file.write(f"File Size: {fileSize}\n")
                file.write(f"Quadrature Rule: {quadRule}\n")
                file.write(f"Order: {order}\n")
                file.write(f"Face Area Calculation Time: {faceAreaCalcTotalTime} seconds\n")
        else:
            # Create a new file with all the timing data
            with open(resultFilePath, 'w') as file:
                file.write(f"File Size: {fileSize}\n")
                file.write(f"Quadrature Rule: {quadRule}\n")
                file.write(f"Order: {order}\n")
                file.write(f"Open Grid Time: {openGridTotalTime} seconds\n")
                file.write(f"Encode As Time: {encodeAsTotalTime} seconds\n")
                file.write(f"Face Area Calculation Time: {faceAreaCalcTotalTime} seconds\n")
                print(f"Timing results saved to: {resultFilePath}")

    else:
        print("File not found. Unable to proceed.")


def plotAreaCalculationComparison(files):
    file_sizes_with_numba = []
    run_times_with_numba = []
    file_sizes_without_numba = []
    run_times_without_numba = []

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

                if "with_numba" in file:
                    file_sizes_with_numba.append(file_size)
                    run_times_with_numba.append(run_time)
                elif "with_out_numba" in file:
                    file_sizes_without_numba.append(file_size)
                    run_times_without_numba.append(run_time)

            except (ValueError, IndexError) as e:
                print(f"Skipping file: {file} - Error: {str(e)}")
                continue

    # Plot both lines on the chart
    fig, ax = plt.subplots()
    ax.plot(file_sizes_with_numba, run_times_with_numba, marker='o', linestyle='-', label="With Numba")
    ax.plot(file_sizes_without_numba, run_times_without_numba, marker='o', linestyle='-', label="Without Numba")
    ax.set_xlabel("File Size")
    ax.set_ylabel("Run Time (seconds)")
    ax.set_title(f"Comparison of First Face Area Calculation Run Times ({quad_rule}, {order})")
    ax.legend()
    ax.set_yscale('log')

    plt.show()


# Running function in loop
for i in ("4KB", "18KB", "98KB", "595KB", "1G", "11G"):
    timingFunction(i, "triangular", 4)

files = ["4KB_with_numba.txt", "18KB_with_numba.txt", "98KB_with_numba.txt", "595KB_with_numba.txt",
         "1G_with_numba.txt", "11G_with_numba.txt", "4KB_with_out_numba.txt", "18KB_with_out_numba.txt",
         "98KB_with_out_numba.txt", "595KB_with_out_numba.txt", "1G_with_out_numba.txt", "11G_with_out_numba.txt"]

plotAreaCalculationComparison(files)

import qupath.lib.images.servers.LabeledImageServer

def imageData = getCurrentImageData()

pathOutputGlob='C:/Users/sdgro/Desktop/TCGA/Tiles/800'

// Define output path (here, relative to project)
def name = GeneralTools.getNameWithoutExtension(imageData.getServer().getMetadata().getName())
def pathOutput = buildFilePath(pathOutputGlob, name)
mkdirs(pathOutput)

// Define output path (relative to project path) for patches generated from annotations with class 'TUMOR'
def pathOutput1= buildFilePath(pathOutput, 'Positive')
mkdirs(pathOutput1)
def server = getCurrentServer()
// Define output resolution
double requestedPixelSize = server.getMetadata()["pixelWidthMicrons"]
//Размер в um
int real_size = 800
// Считаем размер тайла в пикселях
int tile_size = real_size/requestedPixelSize  // tile size under mpp = 0.922
exte = '.jpg' //also png is possible

int overl = 0   // should there be overlap between patches, if yes define oberlap size in pixels

// Convert to downsample
double downsample = requestedPixelSize / imageData.getServer().getPixelCalibration().getAveragedPixelSize()


// Create an ImageServer where the pixels are derived from annotations
def labelServer1 = new LabeledImageServer.Builder(imageData)
    .backgroundLabel(0, ColorTools.WHITE) // Specify background label (usually 0 or 255)
    .downsample(downsample)    // Choose server resolution; this should match the resolution at which tiles are exported
    .addLabel('Positive', 1)      // Choose output labels (the order matters!)
    .multichannelOutput(false)  // If true, each label is a different channel (required for multiclass probability)
    .build()

// Create an exporter that requests corresponding tiles from the original & labeled image servers
new TileExporter(imageData)
    .downsample(downsample)     // Define export resolution
    .imageExtension(exte)     // Define file extension for original pixels (often .tif, .jpg, '.png' or '.ome.tif')
    .tileSize(tile_size)              // Define size of each tile, in pixels
    .labeledServer(labelServer1) // Define the labeled image server to use (i.e. the one we just built)
    .annotatedTilesOnly(false)  // If true, only export tiles if there is a (labeled) annotation present
    .overlap(overl)                // Define overlap, in pixel units at the export resolution
    //.includePartialTiles(true)
    .writeTiles(pathOutput1)     // Write tiles to the specified directory

print 'Done for TUMOR!'




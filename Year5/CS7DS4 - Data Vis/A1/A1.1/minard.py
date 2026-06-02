import processing.javafx.*;

Table table;
float lonMin = 24;
float lonMax = 38;
float latMin = 54;
float latMax = 56;
float survScale = 10000.0;

// vertical layout
float mapTop = 100;
float mapBottom = 400;
float tempGraphTop = mapBottom + 200;
float tempGraphBottom = 750;

void setup() {
  size(1600, 900, FX2D);
  pixelDensity(displayDensity());
  smooth(8);
  background(255);
  textFont(createFont("Arial", 12, true));
  textAlign(CENTER, CENTER);

  table = loadTable("minard-data.csv", "header, csv");

  drawAxes();
  drawTroopPaths();
  drawLegend();
  drawTemperatureGraph();
  drawTemperatureLinks();

  fill(0);
  textSize(18);
  text("Minard’s Map of Napoleon’s Russian Campaign (1812)", width/2, 30);
}

void drawAxes() {
  stroke(0);
  strokeWeight(1);
  fill(0);
  textSize(12);
  textAlign(CENTER);

  // === Troop Map Axes ===
  // X-axis (Longitude)
  line(100, mapBottom + 30, width - 100, mapBottom + 30);
  text("Longitude (°E)", width / 2, mapBottom + 50);

  // Tick marks for longitude
  for (float lon = lonMin; lon <= lonMax; lon += 2) {
    float x = map(lon, lonMin, lonMax, 100, width - 100);
    line(x, mapBottom + 25, x, mapBottom + 35);
    text(nfc(lon, 0), x, mapBottom + 48);
  }

  // Y-axis (Latitude)
  line(80, mapBottom, 80, mapTop);
  textAlign(RIGHT);
  pushMatrix();
  translate(60, (mapTop + mapBottom) / 2);  // move to middle-left of axis
  rotate(-HALF_PI);                         // rotate 90° counterclockwise
  textAlign(CENTER, CENTER);
  text("Latitude (°N)", 0, -25);
  popMatrix();
  textAlign(CENTER);

  // Tick marks for latitude
  for (float lat = latMin; lat <= latMax; lat += 0.5) {
    float y = map(lat, latMin, latMax, mapBottom, mapTop);
    line(75, y, 85, y);
    text(nfc(lat, 1), 60, y);
  }

  // === Temperature Graph Axes ===
  stroke(0);
  line(100, tempGraphBottom, width - 100, tempGraphBottom); // x-axis
  text("Longitude (°E)", width / 2, tempGraphBottom + 35);
  
    // Tick marks for longitude
  for (float lon = lonMin; lon <= lonMax; lon += 2) {
    float x = map(lon, lonMin, lonMax, 100, width - 100);
    line(x, tempGraphBottom-5, x, tempGraphBottom+5);
    text(nfc(lon, 0), x, tempGraphBottom+25);
  }
  
  line(100, tempGraphTop, 100, tempGraphBottom); // y-axis
  textAlign(RIGHT);
  pushMatrix();
  translate(60, (tempGraphTop + tempGraphBottom) / 2);
  rotate(-HALF_PI);
  textAlign(CENTER, CENTER);
  text("Temperature (°C)", 0, -25);
  popMatrix();

  // Tick marks for temperature
  for (int t = -30; t <= 0; t += 5) {
    float y = map(t, -35, 0, tempGraphBottom, tempGraphTop);
    line(95, y, 105, y);
    textAlign(RIGHT);
    text(t, 90, y);
  }
}

void drawTroopPaths() {
  noFill();

  for (int i = 0; i < table.getRowCount() - 1; i++) {
    TableRow row = table.getRow(i);
    TableRow next = table.getRow(i + 1);

    if (row.getString("LONP").equals("") || row.getString("LATP").equals("") ||
      next.getString("LONP").equals("") || next.getString("LATP").equals(""))
      continue;

    float lon1 = row.getFloat("LONP");
    float lat1 = row.getFloat("LATP");
    float lon2 = next.getFloat("LONP");
    float lat2 = next.getFloat("LATP");

    float surv = row.getFloat("SURV");
    String dir = row.getString("DIR");

    float x1 = map(lon1, lonMin, lonMax, 100, width - 100);
    float y1 = map(lat1, latMin, latMax, mapBottom, mapTop);
    float x2 = map(lon2, lonMin, lonMax, 100, width - 100);
    float y2 = map(lat2, latMin, latMax, mapBottom, mapTop);

    if (dir.equals("A")) stroke(210, 180, 140); // advance = tan
    else stroke(0); // retreat = black

    strokeWeight(max(1, surv / survScale));
    line(x1, y1, x2, y2);
  }

  drawCities();
}

void drawCities() {
  fill(0);
  stroke(255, 0, 0);
  textSize(10);
  textAlign(CENTER);

  for (TableRow row : table.rows()) {
    String city = row.getString("CITY");
    int wrdlen = city.length();
    String lonC = row.getString("LONC");
    String latC = row.getString("LATC");

    if (!city.equals("") && !lonC.equals("") && !latC.equals("")) {
      float x = map(row.getFloat("LONC"), lonMin, lonMax, 100, width - 100);
      float y = map(row.getFloat("LATC"), latMin, latMax, mapBottom, mapTop);
      ellipse(x, y, 4, 4);
      fill(255, 255, 255);
      rect(x-(3*wrdlen), y-20, (wrdlen*6), 10);
      fill(255, 0, 0);
      text(city, x, y - 10);
    }
  }
}

void drawTemperatureGraph() {
  fill(0, 0, 255);
  textSize(12);

  float prevX = -1, prevY = -1;

  for (TableRow row : table.rows()) {
    String tempStr = row.getString("TEMP");
    String lontStr = row.getString("LONT");

    if (tempStr.equals("") || lontStr.equals("")) continue;

    float temp = row.getFloat("TEMP");
    float lon = row.getFloat("LONT");

    float x = map(lon, lonMin, lonMax, 100, width - 100);
    float y = map(temp, -35, 0, tempGraphBottom, tempGraphTop);

    ellipse(x, y, 6, 6);

    if (prevX > 0) {
      stroke(0, 0, 255);
      line(prevX, prevY, x, y);
    }

    prevX = x;
    prevY = y;

    textAlign(CENTER, BOTTOM);
    String dayStr = row.getString("DAY");
    String monStr = row.getString("MON");

    String tempLabel = nfc(temp, 0) + "°";
    String dateLabel = (!dayStr.equals("") && !monStr.equals("")) ? (dayStr + " " + monStr) : "";

    float labelOffset = 10;  // pixels above the point

    text(tempLabel, x, y - labelOffset);
    if (!dateLabel.equals("")) {
      textSize(10); // slightly smaller for date
      text(dateLabel, x, y - labelOffset - 15);
      textSize(12); // restore default for next loop
    }
  }
}

void drawTemperatureLinks() {
  stroke(100, 100, 100, 180); // semi-transparent grey
  strokeWeight(1);

  // --- Extract retreat data points (longitude, latitude) ---
  ArrayList<Float> retreatLons = new ArrayList<Float>();
  ArrayList<Float> retreatLats = new ArrayList<Float>();

  for (TableRow row : table.rows()) {
    if (row.getString("DIR").equals("R") && !row.getString("LONP").equals("") && !row.getString("LATP").equals("")) {
      retreatLons.add(row.getFloat("LONP"));
      retreatLats.add(row.getFloat("LATP"));
    }
  }

  // --- Draw lines for each temperature point ---
  for (TableRow row : table.rows()) {
    String tempStr = row.getString("TEMP");
    String lonStr = row.getString("LONT");
    if (tempStr.equals("") || lonStr.equals("")) continue;

    float lonT = row.getFloat("LONT");
    float temp = row.getFloat("TEMP");

    // find two retreat points around this longitude
    float latInterp = Float.NaN;
    for (int i = 0; i < retreatLons.size() - 1; i++) {
      float lon1 = retreatLons.get(i);
      float lon2 = retreatLons.get(i + 1);
      if ((lonT >= lon1 && lonT <= lon2) || (lonT <= lon1 && lonT >= lon2)) {
        float lat1 = retreatLats.get(i);
        float lat2 = retreatLats.get(i + 1);
        float inter = map(lonT, lon1, lon2, 0, 1);
        latInterp = lerp(lat1, lat2, inter);
        break;
      }
    }

    if (Float.isNaN(latInterp)) continue; // skip if out of range

    // map coordinates to screen
    float x = map(lonT, lonMin, lonMax, 100, width - 100);
    float yMap = map(latInterp, latMin, latMax, mapBottom, mapTop);
    float yTemp = map(temp, -35, 0, tempGraphBottom, tempGraphTop);

    line(x, yMap, x, yTemp);
  }
}

void drawLegend() {
  float lgndX = width - 525;
  float lgndY = height * 0.325;
  float lgndW = 200;
  float lgndH = 120;

  fill(255); // Set fill to white
  stroke(0);
  rect(lgndX, lgndY, lgndW, lgndH);
  fill(0);
  textAlign(LEFT);
  textSize(12);


  //legend & labels
  fill(210, 180, 140); // tan
  rect(lgndX+10, lgndY+10, 10, 10);
  fill(0);
  text("Advance", lgndX+30, lgndY+20);

  fill(0);
  rect(lgndX+10, lgndY+30, 10, 10);
  fill(0);
  text("Retreat", lgndX+30, lgndY+40);

  // --- Troop Strength Triangle ---
  float triX1 = lgndX + 20;   // left base (wide end)
  float triX2 = lgndX + 180;  // right tip (narrow end)
  float triY = lgndY + 80;
  float triBaseMax = 34;      // width of wide end
  float triBaseMin = 0.6;       // width of narrow end

  // Draw gradient manually
  int steps = int(triX2 - triX1);
  for (int i = 0; i <= steps; i++) {
    float inter = map(i, 0, steps, 0, 1);
    // Interpolate between tan (210,180,140) and black (0,0,0)
    float r = lerp(210, 0, inter);
    float g = lerp(180, 0, inter);
    float b = lerp(140, 0, inter);
    fill(r, g, b);
    noStroke();

    float x = triX1 + i;
    // Interpolate triangle width (taper)
    float baseWidth = lerp(triBaseMax, triBaseMin, inter);
    rect(x, triY - baseWidth/2, 1, baseWidth);
  }

  noStroke();
  noFill();
  beginShape();
  vertex(triX1, triY - triBaseMax/2);
  vertex(triX1, triY + triBaseMax/2);
  vertex(triX2, triY + triBaseMin/2);
  vertex(triX2, triY - triBaseMin/2);
  endShape(CLOSE);

  fill(0);
  textSize(11);
  textAlign(CENTER);
  text("Troop strength scale", (lgndX + lgndW / 2), triY - 20);

  textAlign(LEFT);
  text("340,000", triX1 - 5, triY + triBaseMax/2 + 15);
  textAlign(RIGHT);
  text("6,000", triX2 + 5, triY + triBaseMin/2 + 15);
}
// Prometheus Course Generation System 2.0 - Figma UI Generator
// Run this plugin in Figma to generate the complete UI
// Aligned with Global UI Contract (PROMETHEUS_UI_SPEC.md)

// ============================================
// COLOR PALETTE - Global UI Contract Compliant
// ============================================
const COLORS = {
  // Core backgrounds
  prometheusBlack: { r: 0.039, g: 0.039, b: 0.039 },     // #0A0A0A - Global background
  panelFill: { r: 0.039, g: 0.039, b: 0.039 },           // #0A0A0A - Panel interior (dark glass)
  inputBg: { r: 0.078, g: 0.086, b: 0.094 },             // #141618 - Input field backgrounds
  
  // Primary accents
  neonBlue: { r: 0.0, g: 0.898, b: 1.0 },                // #00E5FF - Primary borders, frames
  glowYellow: { r: 1.0, g: 0.851, b: 0.4 },              // #FFD966 - AI panel borders, highlights
  
  // Button gradient colors
  glassSilverLight: { r: 0.749, g: 0.757, b: 0.776 },    // #BFC1C6 - Button gradient top
  glassSilverDark: { r: 0.549, g: 0.557, b: 0.573 },     // #8C8E92 - Button gradient bottom
  
  // Disabled button colors
  disabledLight: { r: 0.35, g: 0.35, b: 0.35 },          // Disabled gradient top
  disabledDark: { r: 0.25, g: 0.25, b: 0.25 },           // Disabled gradient bottom
  
  // Text colors
  pureWhite: { r: 1, g: 1, b: 1 },                       // #FFFFFF - Primary text
  softGrey: { r: 0.780, g: 0.780, b: 0.780 },            // #C7C7C7 - Secondary text
  inactiveGrey: { r: 0.306, g: 0.306, b: 0.306 },        // #4E4E4E - Disabled elements
  
  // Status colors
  approvedGreen: { r: 0.290, g: 1.0, b: 0.502 },         // #4AFF80 - Approved flag
  statusGreen: { r: 0.0, g: 0.831, b: 0.329 },           // #00D454 - General status values
  hoverGreen: { r: 0.2, g: 0.9, b: 0.4 },                // Hover state green
  dragGreen: { r: 0.4, g: 1.0, b: 0.6 },                 // Luminous drag state green
  editOrange: { r: 1.0, g: 0.6, b: 0.2 },                // Edit state orange
  
  // Legacy compatibility (will be phased out)
  buttonBorder: { r: 1, g: 1, b: 1 },                    // #FFFFFF - Button border (white per spec)
};

// ============================================
// HELPER FUNCTIONS
// ============================================

function rgbToFigma(color) {
  return { r: color.r, g: color.g, b: color.b };
}

function createSolidPaint(color, opacity = 1) {
  return [{ type: 'SOLID', color: rgbToFigma(color), opacity: opacity }];
}

function createGradientPaint(colorTop, colorBottom) {
  return [{
    type: 'GRADIENT_LINEAR',
    gradientStops: [
      { position: 0, color: { r: colorTop.r, g: colorTop.g, b: colorTop.b, a: 1 } },
      { position: 1, color: { r: colorBottom.r, g: colorBottom.g, b: colorBottom.b, a: 1 } }
    ],
    gradientTransform: [[0, 1, 0], [-1, 0, 1]]  // Vertical gradient (top to bottom)
  }];
}

async function loadFonts() {
  // Load fonts - using Inter as Figma-available fallback for Bahnschrift
  // Spec: Bahnschrift SemiCondensed → Segoe UI → Arial
  await figma.loadFontAsync({ family: "Inter", style: "Regular" });
  await figma.loadFontAsync({ family: "Inter", style: "Medium" });
  await figma.loadFontAsync({ family: "Inter", style: "SemiBold" });
  await figma.loadFontAsync({ family: "Inter", style: "Bold" });
}

function createText(text, x, y, fontSize, color, fontStyle = "Regular", letterSpacing = 0) {
  const textNode = figma.createText();
  textNode.x = x;
  textNode.y = y;
  textNode.fontName = { family: "Inter", style: fontStyle };
  textNode.fontSize = fontSize;
  textNode.characters = text;
  textNode.fills = createSolidPaint(color);
  if (letterSpacing > 0) {
    textNode.letterSpacing = { value: letterSpacing, unit: "PERCENT" };
  }
  return textNode;
}

function createRoundedRect(x, y, width, height, cornerRadius, fillColor, strokeColor = null, strokeWeight = 0, fillOpacity = 1) {
  const rect = figma.createRectangle();
  rect.x = x;
  rect.y = y;
  rect.resize(width, height);
  rect.cornerRadius = cornerRadius;
  rect.fills = createSolidPaint(fillColor, fillOpacity);
  
  if (strokeColor && strokeWeight > 0) {
    rect.strokes = createSolidPaint(strokeColor);
    rect.strokeWeight = strokeWeight;
  }
  
  return rect;
}

function createGradientRect(x, y, width, height, cornerRadius, colorTop, colorBottom, strokeColor = null, strokeWeight = 0) {
  const rect = figma.createRectangle();
  rect.x = x;
  rect.y = y;
  rect.resize(width, height);
  rect.cornerRadius = cornerRadius;
  rect.fills = createGradientPaint(colorTop, colorBottom);
  
  if (strokeColor && strokeWeight > 0) {
    rect.strokes = createSolidPaint(strokeColor);
    rect.strokeWeight = strokeWeight;
  }
  
  return rect;
}

function createFrame(name, x, y, width, height) {
  const frame = figma.createFrame();
  frame.name = name;
  frame.x = x;
  frame.y = y;
  frame.resize(width, height);
  frame.fills = [];
  frame.clipsContent = false;
  return frame;
}

function createLine(x1, y1, x2, y2, color, strokeWeight = 2, opacity = 0.7) {
  const line = figma.createLine();
  line.x = x1;
  line.y = y1;
  line.rotation = Math.atan2(y2 - y1, x2 - x1) * (180 / Math.PI);
  const length = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
  line.resize(length, 0);
  line.strokes = createSolidPaint(color, opacity);
  line.strokeWeight = strokeWeight;
  return line;
}

function createCircle(x, y, diameter, fillColor, strokeColor = null, strokeWeight = 0) {
  const circle = figma.createEllipse();
  circle.x = x;
  circle.y = y;
  circle.resize(diameter, diameter);
  circle.fills = createSolidPaint(fillColor);
  if (strokeColor && strokeWeight > 0) {
    circle.strokes = createSolidPaint(strokeColor);
    circle.strokeWeight = strokeWeight;
  }
  return circle;
}

// Add glow effect to a node
function addGlowEffect(node, color, blur = 28, opacity = 0.25) {
  node.effects = [
    {
      type: 'DROP_SHADOW',
      color: { r: color.r, g: color.g, b: color.b, a: opacity },
      offset: { x: 0, y: 0 },
      radius: blur,
      spread: 0,
      visible: true,
      blendMode: 'NORMAL'
    }
  ];
}

// Add inner shadow effect to a node
function addInnerShadow(node, opacity = 0.2, blur = 12) {
  const existingEffects = node.effects || [];
  node.effects = [
    ...existingEffects,
    {
      type: 'INNER_SHADOW',
      color: { r: 0, g: 0, b: 0, a: opacity },
      offset: { x: 0, y: 2 },
      radius: blur,
      spread: 0,
      visible: true,
      blendMode: 'NORMAL'
    }
  ];
}

// ============================================
// UI COMPONENT BUILDERS
// ============================================

// 3D Glass Button - Per Global UI Contract Section 1.5
function createGlassButton(name, x, y, width, height, label, cornerRadius = 24) {
  const buttonFrame = createFrame(name, x, y, width, height);
  
  // Button background with silver gradient
  const bg = createGradientRect(0, 0, width, height, cornerRadius, 
    COLORS.glassSilverLight, COLORS.glassSilverDark, 
    COLORS.pureWhite, 2);
  bg.name = "Btn_Background";
  
  // Add inner shadow for glass effect
  addInnerShadow(bg, 0.15, 4);
  
  buttonFrame.appendChild(bg);
  
  // Button label - Spec: 16-18px, SemiBold, UPPERCASE
  const lines = label.split('\n');
  const lineHeight = 18;
  const totalTextHeight = lines.length * lineHeight;
  const startY = (height - totalTextHeight) / 2;
  
  lines.forEach((line, i) => {
    const labelText = createText(line.toUpperCase(), 0, startY + (i * lineHeight), 16, COLORS.pureWhite, "SemiBold", 10);
    labelText.name = `Label_Line${i + 1}`;
    labelText.textAlignHorizontal = "CENTER";
    labelText.resize(width, lineHeight);
    buttonFrame.appendChild(labelText);
  });
  
  return buttonFrame;
}

// Small glass button for top bar (Load, Save, Delete, Reset)
function createSmallGlassButton(name, x, y, width, height, label, disabled = false) {
  const buttonFrame = createFrame(name, x, y, width, height);
  
  // Button background - use disabled colors if disabled
  const colorTop = disabled ? COLORS.disabledLight : COLORS.glassSilverLight;
  const colorBottom = disabled ? COLORS.disabledDark : COLORS.glassSilverDark;
  const strokeColor = disabled ? COLORS.inactiveGrey : COLORS.pureWhite;
  const textColor = disabled ? COLORS.inactiveGrey : COLORS.pureWhite;
  
  const bg = createGradientRect(0, 0, width, height, 12, colorTop, colorBottom, strokeColor, 2);
  bg.name = "Btn_Background";
  if (!disabled) {
    addInnerShadow(bg, 0.15, 3);
  }
  buttonFrame.appendChild(bg);
  
  // Button label
  const labelText = createText(label.toUpperCase(), 0, 0, 14, textColor, "SemiBold", 8);
  labelText.name = "Label";
  labelText.textAlignHorizontal = "CENTER";
  labelText.textAlignVertical = "CENTER";
  labelText.resize(width, height);
  buttonFrame.appendChild(labelText);
  
  return buttonFrame;
}

// Small segmented button for edit tools
function createSegmentedButton(name, x, y, width, height, label) {
  const buttonFrame = createFrame(name, x, y, width, height);
  
  const bg = createRoundedRect(0, 0, width, height, 8, COLORS.prometheusBlack, COLORS.softGrey, 1, 0.8);
  bg.name = "Btn_Background";
  buttonFrame.appendChild(bg);
  
  const labelText = createText(label.toUpperCase(), 0, 0, 10, COLORS.softGrey, "Medium", 5);
  labelText.name = "Label";
  labelText.textAlignHorizontal = "CENTER";
  labelText.textAlignVertical = "CENTER";
  labelText.resize(width, height);
  buttonFrame.appendChild(labelText);
  
  return buttonFrame;
}

function createInputField(name, x, y, width, height = 28) {
  const inputFrame = createFrame(name, x, y, width, height);
  
  const bg = createRoundedRect(0, 0, width, height, 4, COLORS.inputBg, COLORS.neonBlue, 1, 0.7);
  bg.name = "Input_Background";
  inputFrame.appendChild(bg);
  
  return inputFrame;
}

// Panel with glow and inner shadow - Per Global UI Contract Section 1.4
function createPanel(name, x, y, width, height, title, strokeColor, cornerRadius = 28) {
  const panelFrame = createFrame(name, x, y, width, height);
  
  // Panel background - Spec: #0A0A0A fill, 4px stroke, 24-30px radius
  const bg = createRoundedRect(0, 0, width, height, cornerRadius, COLORS.panelFill, strokeColor, 4);
  bg.name = "Panel_Background";
  
  // Add outer glow - Spec: same color as stroke, 24-32px blur, 20-35% opacity
  addGlowEffect(bg, strokeColor, 28, 0.25);
  
  // Add inner shadow - Spec: black 20%, 12px blur, inset
  addInnerShadow(bg, 0.2, 12);
  
  panelFrame.appendChild(bg);
  
  // Panel title
  if (title) {
    const titleText = createText(title.toUpperCase(), 20, 16, 18, COLORS.pureWhite, "SemiBold", 15);
    titleText.name = "Label_Title";
    panelFrame.appendChild(titleText);
  }
  
  return panelFrame;
}

// Small panel for warnings
function createSmallPanel(name, x, y, width, height, title, strokeColor, cornerRadius = 16) {
  const panelFrame = createFrame(name, x, y, width, height);
  
  const bg = createRoundedRect(0, 0, width, height, cornerRadius, COLORS.panelFill, strokeColor, 2);
  bg.name = "Panel_Background";
  addGlowEffect(bg, strokeColor, 16, 0.2);
  panelFrame.appendChild(bg);
  
  if (title) {
    const titleText = createText(title.toUpperCase(), 12, 10, 12, COLORS.pureWhite, "SemiBold", 10);
    titleText.name = "Label_Title";
    panelFrame.appendChild(titleText);
  }
  
  return panelFrame;
}

function createLearningObjectiveItem(index, x, y, width, height) {
  const itemFrame = createFrame(`Item_Objective${index}`, x, y, width, height);
  
  // Item background
  const bg = createRoundedRect(0, 0, width, height, 12, COLORS.prometheusBlack, COLORS.softGrey, 1, 0.8);
  bg.name = "Item_Background";
  itemFrame.appendChild(bg);
  
  // Index number
  const indexText = createText(String(index), 12, 10, 14, COLORS.softGrey, "Medium");
  indexText.name = "Label_Index";
  itemFrame.appendChild(indexText);
  
  // Plus button
  const plusText = createText("+", width - 30, 10, 16, COLORS.softGrey, "Medium");
  plusText.name = "Btn_Add";
  itemFrame.appendChild(plusText);
  
  return itemFrame;
}

// Manager node button with 3D glass effect
function createManagerNode(name, x, y, width, height, label) {
  const nodeFrame = createFrame(name, x, y, width, height);
  
  // Node background with glass gradient
  const bg = createGradientRect(0, 0, width, height, 20, 
    COLORS.glassSilverLight, COLORS.glassSilverDark, 
    COLORS.pureWhite, 2);
  bg.name = "Node_Background";
  addInnerShadow(bg, 0.15, 4);
  addGlowEffect(bg, COLORS.neonBlue, 16, 0.15);
  nodeFrame.appendChild(bg);
  
  // Split label into lines
  const lines = label.split('\n');
  const lineHeight = 18;
  const startY = (height - (lines.length * lineHeight)) / 2;
  
  lines.forEach((line, i) => {
    const text = createText(line.toUpperCase(), 0, startY + (i * lineHeight), 15, COLORS.pureWhite, "SemiBold", 10);
    text.name = `Label_Line${i + 1}`;
    text.textAlignHorizontal = "CENTER";
    text.resize(width, lineHeight);
    nodeFrame.appendChild(text);
  });
  
  return nodeFrame;
}

// PKE Icon (flame/fire icon)
function createPKEIcon(name, x, y, size, isGold = true) {
  const iconFrame = createFrame(name, x, y, size, size);
  const color = isGold ? COLORS.glowYellow : COLORS.neonBlue;
  
  const iconText = createText("🔥", 0, 0, size - 4, color, "Regular");
  iconText.name = "Icon";
  iconFrame.appendChild(iconText);
  
  return iconFrame;
}

// ============================================
// SCALAR MANAGER COMPONENTS
// ============================================

// Scalar row item with different states
function createScalarRow(name, x, y, width, height, serial, text, state = "normal") {
  const rowFrame = createFrame(name, x, y, width, height);
  
  let textColor = COLORS.pureWhite;
  let serialColor = COLORS.softGrey;
  let strokeColor = COLORS.neonBlue;
  let strokeOpacity = 0.5;
  
  switch(state) {
    case "hover":
      textColor = COLORS.hoverGreen;
      serialColor = COLORS.hoverGreen;
      strokeColor = COLORS.hoverGreen;
      strokeOpacity = 0.7;
      break;
    case "drag":
      textColor = COLORS.dragGreen;
      serialColor = COLORS.dragGreen;
      strokeColor = COLORS.dragGreen;
      strokeOpacity = 1.0;
      break;
    case "edit":
      textColor = COLORS.editOrange;
      serialColor = COLORS.editOrange;
      strokeColor = COLORS.editOrange;
      strokeOpacity = 0.8;
      break;
  }
  
  // Row background
  const bg = createRoundedRect(0, 0, width, height, 6, COLORS.prometheusBlack, strokeColor, 1, 0.7);
  bg.name = "Row_Background";
  if (state === "drag") {
    addGlowEffect(bg, COLORS.dragGreen, 8, 0.4);
  }
  rowFrame.appendChild(bg);
  
  // Serial number
  const serialText = createText(serial, 8, (height - 12) / 2, 11, serialColor, "Medium");
  serialText.name = "Label_Serial";
  rowFrame.appendChild(serialText);
  
  // Text content
  const contentText = createText(text, 45, (height - 12) / 2, 11, textColor, "Regular");
  contentText.name = "Label_Content";
  rowFrame.appendChild(contentText);
  
  // Edit state icons (confirm/cancel)
  if (state === "edit") {
    const confirmIcon = createText("✔", width - 35, (height - 12) / 2, 12, COLORS.statusGreen, "Medium");
    confirmIcon.name = "Btn_Confirm";
    rowFrame.appendChild(confirmIcon);
    
    const cancelIcon = createText("✖", width - 18, (height - 12) / 2, 12, { r: 0.9, g: 0.2, b: 0.2 }, "Medium");
    cancelIcon.name = "Btn_Cancel";
    rowFrame.appendChild(cancelIcon);
  }
  
  return rowFrame;
}

// Scalar column with header, content area, and entry row
function createScalarColumn(name, x, y, width, height, label, count = 0) {
  const colFrame = createFrame(name, x, y, width, height);
  
  // Column background
  const bg = createRoundedRect(0, 0, width, height, 16, COLORS.panelFill, COLORS.neonBlue, 2);
  bg.name = "Column_Background";
  addGlowEffect(bg, COLORS.neonBlue, 12, 0.15);
  colFrame.appendChild(bg);
  
  // Header area
  const headerBg = createRoundedRect(0, 0, width, 36, 16, COLORS.prometheusBlack, null, 0, 0.5);
  // Fix corner radius for top only
  headerBg.topLeftRadius = 16;
  headerBg.topRightRadius = 16;
  headerBg.bottomLeftRadius = 0;
  headerBg.bottomRightRadius = 0;
  headerBg.name = "Header_Background";
  colFrame.appendChild(headerBg);
  
  // Column label
  const labelText = createText(label.toUpperCase(), 10, 10, 11, COLORS.pureWhite, "SemiBold", 8);
  labelText.name = "Label_Header";
  colFrame.appendChild(labelText);
  
  // PKE icon
  const pkeIcon = createPKEIcon("Icon_PKE_" + label.replace(/\s/g, ''), width - 32, 8, 18, true);
  colFrame.appendChild(pkeIcon);
  
  // Counter
  const counterText = createText(`(${count})`, width - 50, 10, 11, COLORS.softGrey, "Regular");
  counterText.name = "Label_Counter";
  colFrame.appendChild(counterText);
  
  // Content area with sample rows showing different states
  const contentY = 42;
  const rowHeight = 28;
  const rowGap = 4;
  
  // Sample rows demonstrating states
  if (label === "CLOs") {
    const row1 = createScalarRow("Row_1_Normal", 6, contentY, width - 12, rowHeight, "1", "Sample CLO text...", "normal");
    colFrame.appendChild(row1);
    
    const row2 = createScalarRow("Row_2_Hover", 6, contentY + rowHeight + rowGap, width - 12, rowHeight, "2", "Hover state example", "hover");
    colFrame.appendChild(row2);
    
    const row3 = createScalarRow("Row_3_Drag", 6, contentY + (rowHeight + rowGap) * 2, width - 12, rowHeight, "3", "Drag state example", "drag");
    colFrame.appendChild(row3);
    
    const row4 = createScalarRow("Row_4_Edit", 6, contentY + (rowHeight + rowGap) * 3, width - 12, rowHeight, "4", "Edit state example", "edit");
    colFrame.appendChild(row4);
  } else {
    // Empty state for other columns
    const emptyText = createText("No items", width / 2 - 25, height / 2 - 10, 11, COLORS.inactiveGrey, "Regular");
    emptyText.name = "Label_Empty";
    colFrame.appendChild(emptyText);
  }
  
  // Data entry row at bottom
  const entryY = height - 34;
  const entryBg = createRoundedRect(6, entryY, width - 12, 28, 6, COLORS.inputBg, COLORS.neonBlue, 1, 0.6);
  entryBg.name = "Input_Entry";
  colFrame.appendChild(entryBg);
  
  // Entry placeholder
  const entryPlaceholder = createText("+ Add new...", 14, entryY + 7, 10, COLORS.inactiveGrey, "Regular");
  entryPlaceholder.name = "Label_EntryPlaceholder";
  colFrame.appendChild(entryPlaceholder);
  
  return colFrame;
}

// ============================================
// MAIN UI SECTIONS
// ============================================

// Layout constants - Per Global UI Contract Section 1.1
const MARGIN = 40;  // Spec: 32-48px outer margin
const FRAME_WIDTH = 1520;
const FRAME_HEIGHT = 900;

function createHeader(parent, pageTitle = null) {
  const headerFrame = createFrame("Global/TopBar", 0, 0, FRAME_WIDTH, 70);
  
  // Subtle neon-blue outline - Spec: 1-2px
  const headerBg = createRoundedRect(0, 0, FRAME_WIDTH, 70, 0, COLORS.prometheusBlack, COLORS.neonBlue, 1, 0.3);
  headerBg.name = "TopBar_Background";
  headerFrame.appendChild(headerBg);
  
  // Logo placeholder (flame icon area)
  const logoRect = createRoundedRect(MARGIN, 10, 44, 50, 8, COLORS.prometheusBlack, COLORS.neonBlue, 2);
  logoRect.name = "Logo_Placeholder";
  addGlowEffect(logoRect, COLORS.neonBlue, 12, 0.3);
  headerFrame.appendChild(logoRect);
  
  // Main title - Spec: 18-24px, SemiBold, UPPERCASE
  const title = createText("PROMETHEUS COURSE", MARGIN + 60, 12, 22, COLORS.pureWhite, "Bold", 8);
  title.name = "Label_Title1";
  headerFrame.appendChild(title);
  
  const subtitle = createText("GENERATION SYSTEM 2.0", MARGIN + 60, 38, 22, COLORS.pureWhite, "Bold", 8);
  subtitle.name = "Label_Title2";
  headerFrame.appendChild(subtitle);
  
  // Page title if provided
  if (pageTitle) {
    const pageTitleText = createText(pageTitle.toUpperCase(), 400, 25, 18, COLORS.neonBlue, "SemiBold", 10);
    pageTitleText.name = "Label_PageTitle";
    headerFrame.appendChild(pageTitleText);
  }
  
  parent.appendChild(headerFrame);
  return headerFrame;
}

function createStatusInfo(parent) {
  const statusFrame = createFrame("Global/StatusInfo", MARGIN, 78, 420, 70);
  
  // Date/Time
  const dateTime = createText("26/11/25    09:25:43", 0, 0, 12, COLORS.neonBlue, "Medium");
  dateTime.name = "Label_DateTime";
  statusFrame.appendChild(dateTime);
  
  // Status items
  const statusItems = [
    { label: "Course Loaded:", value: "Example", y: 18 },
    { label: "Duration:", value: "3 Days", y: 32 },
    { label: "Level:", value: "Basic", y: 46 },
    { label: "Thematic:", value: "Intelligence", y: 60 },
  ];
  
  statusItems.forEach(item => {
    const label = createText(item.label, 0, item.y, 11, COLORS.softGrey, "Regular");
    label.name = `Label_${item.label.replace(':', '')}`;
    statusFrame.appendChild(label);
    
    const value = createText(item.value, 100, item.y, 11, COLORS.statusGreen, "Medium");
    value.name = `Value_${item.label.replace(':', '')}`;
    statusFrame.appendChild(value);
  });
  
  parent.appendChild(statusFrame);
  return statusFrame;
}

function createLearningObjectivesPanel(parent) {
  // Left column (30%) - Spec Template A
  const panelFrame = createPanel("Dashboard/Panel_LearningObjectives", MARGIN, 155, 400, 520, null, COLORS.neonBlue, 28);
  
  // Header - Spec: 18-24px, SemiBold, UPPERCASE
  const header = createText("LEARNING OBJECTIVES", 24, 20, 16, COLORS.pureWhite, "SemiBold", 12);
  header.name = "Label_Header";
  panelFrame.appendChild(header);
  
  // Refresh icon placeholder
  const refreshIcon = createText("↻", 355, 20, 18, COLORS.softGrey, "Regular");
  refreshIcon.name = "Btn_Refresh";
  panelFrame.appendChild(refreshIcon);
  
  // Objective items
  for (let i = 1; i <= 3; i++) {
    const item = createLearningObjectiveItem(i, 20, 55 + ((i - 1) * 95), 355, 85);
    panelFrame.appendChild(item);
  }
  
  // Scrollbar track
  const scrollTrack = createRoundedRect(375, 55, 6, 440, 3, COLORS.inactiveGrey, null, 0, 0.4);
  scrollTrack.name = "Scroll_Track";
  panelFrame.appendChild(scrollTrack);
  
  // Scrollbar thumb
  const scrollThumb = createRoundedRect(375, 55, 6, 140, 3, COLORS.statusGreen);
  scrollThumb.name = "Scroll_Thumb";
  panelFrame.appendChild(scrollThumb);
  
  parent.appendChild(panelFrame);
  return panelFrame;
}

function createCourseSelectionArea(parent) {
  const selectionFrame = createFrame("Dashboard/CourseSelection", 460, MARGIN, 560, 55);
  
  // Label - Spec: Secondary text uses Soft Grey
  const label = createText("SELECT COURSE:", 0, 0, 13, COLORS.softGrey, "SemiBold", 10);
  label.name = "Label_SelectCourse";
  selectionFrame.appendChild(label);
  
  // Dropdown
  const dropdown = createInputField("Input_CourseDropdown", 0, 24, 560, 32);
  selectionFrame.appendChild(dropdown);
  
  parent.appendChild(selectionFrame);
  return selectionFrame;
}

function createTopBarButtons(parent, disableLoadDelete = false) {
  // Spec: small glass buttons (Load, Save, Delete, Reset) - 80-100px width
  const buttonsFrame = createFrame("Global/TopBarActions", FRAME_WIDTH - MARGIN - 440, 15, 440, 45);
  
  const loadBtn = createSmallGlassButton("Btn_Load", 0, 0, 90, 40, "LOAD", disableLoadDelete);
  buttonsFrame.appendChild(loadBtn);
  
  const saveBtn = createSmallGlassButton("Btn_Save", 110, 0, 90, 40, "SAVE", false);
  buttonsFrame.appendChild(saveBtn);
  
  const deleteBtn = createSmallGlassButton("Btn_Delete", 220, 0, 90, 40, "DELETE", disableLoadDelete);
  buttonsFrame.appendChild(deleteBtn);
  
  // On Scalar Manager, this is CLEAR instead of RESET
  const resetLabel = disableLoadDelete ? "CLEAR" : "RESET";
  const resetBtn = createSmallGlassButton("Btn_Reset", 330, 0, 90, 40, resetLabel, false);
  buttonsFrame.appendChild(resetBtn);
  
  parent.appendChild(buttonsFrame);
  return buttonsFrame;
}

function createCourseInformationPanel(parent) {
  // Center column element 1
  const panelFrame = createPanel("Dashboard/Panel_CourseInfo", 460, 105, 560, 200, null, COLORS.neonBlue, 24);
  
  // Header - Spec: centered, Neon Blue color
  const header = createText("COURSE INFORMATION", 0, 14, 16, COLORS.neonBlue, "SemiBold", 12);
  header.name = "Label_Header";
  header.textAlignHorizontal = "CENTER";
  header.resize(560, 24);
  panelFrame.appendChild(header);
  
  // Form fields
  const fields = [
    { label: "Title:", y: 50 },
    { label: "Level:", y: 80 },
    { label: "Thematic:", y: 110 },
    { label: "Duration:", y: 140, hasCode: true },
    { label: "Developer:", y: 170 },
  ];
  
  fields.forEach(field => {
    const label = createText(field.label, 28, field.y, 13, COLORS.pureWhite, "Regular");
    label.name = `Label_${field.label.replace(':', '')}`;
    panelFrame.appendChild(label);
    
    if (field.hasCode) {
      const input = createInputField(`Input_${field.label.replace(':', '')}`, 115, field.y - 4, 175, 26);
      panelFrame.appendChild(input);
      
      const codeLabel = createText("Code:", 310, field.y, 13, COLORS.pureWhite, "Regular");
      codeLabel.name = "Label_Code";
      panelFrame.appendChild(codeLabel);
      
      const codeInput = createInputField("Input_Code", 365, field.y - 4, 175, 26);
      panelFrame.appendChild(codeInput);
    } else {
      const input = createInputField(`Input_${field.label.replace(':', '')}`, 115, field.y - 4, 425, 26);
      panelFrame.appendChild(input);
    }
  });
  
  parent.appendChild(panelFrame);
  return panelFrame;
}

function createCourseDescriptionPanel(parent) {
  // Center column element 2
  const panelFrame = createPanel("Dashboard/Panel_CourseDescription", 460, 315, 560, 200, null, COLORS.neonBlue, 24);
  
  // Header
  const header = createText("COURSE DESCRIPTION", 0, 14, 16, COLORS.pureWhite, "SemiBold", 12);
  header.name = "Label_Header";
  header.textAlignHorizontal = "CENTER";
  header.resize(560, 24);
  panelFrame.appendChild(header);
  
  // Refresh/PKE icon
  const refreshIcon = createText("🔥", 515, 12, 16, COLORS.glowYellow, "Regular");
  refreshIcon.name = "Btn_PKE";
  panelFrame.appendChild(refreshIcon);
  
  // Text area background
  const textArea = createRoundedRect(24, 45, 512, 140, 12, COLORS.prometheusBlack, COLORS.softGrey, 1, 0.5);
  textArea.name = "Input_Description";
  panelFrame.appendChild(textArea);
  
  parent.appendChild(panelFrame);
  return panelFrame;
}

function createManagerNodes(parent) {
  // Center column element 3 - Node row
  const nodesFrame = createFrame("Dashboard/NodeRow_Managers", 460, 525, 560, 100);
  
  const nodeWidth = 160;
  const nodeHeight = 90;
  const gap = 40;
  
  const managers = [
    { name: "Node_ScalarManager", label: "SCALAR\nMANAGER", x: 0 },
    { name: "Node_ContentManager", label: "CONTENT\nMANAGER", x: nodeWidth + gap },
    { name: "Node_LessonManager", label: "LESSON\nMANAGER", x: (nodeWidth + gap) * 2 },
  ];
  
  managers.forEach(manager => {
    const node = createManagerNode(manager.name, manager.x, 0, nodeWidth, nodeHeight, manager.label);
    nodesFrame.appendChild(node);
  });
  
  parent.appendChild(nodesFrame);
  return nodesFrame;
}

function createAIConsole(parent, yOffset = 635) {
  // Spec Section 1.8: 140-160px height, 28-32px radius, 4px Glow Yellow stroke
  const aiFrame = createFrame("Global/AIConsole", MARGIN, yOffset, FRAME_WIDTH - (MARGIN * 2), 150);
  
  // Background with yellow/gold accent
  const bg = createRoundedRect(0, 0, FRAME_WIDTH - (MARGIN * 2), 150, 28, { r: 0, g: 0, b: 0 }, COLORS.glowYellow, 4);
  bg.name = "Console_Background";
  addGlowEffect(bg, COLORS.glowYellow, 28, 0.25);
  addInnerShadow(bg, 0.2, 12);
  aiFrame.appendChild(bg);
  
  // Header
  const header = createText("PROMETHEUS AI", 0, 14, 14, COLORS.softGrey, "SemiBold", 10);
  header.name = "Label_Header";
  header.textAlignHorizontal = "CENTER";
  header.resize(FRAME_WIDTH - (MARGIN * 2), 20);
  aiFrame.appendChild(header);
  
  // Chat/terminal area - Spec: Monospace green terminal font
  const chatArea = createRoundedRect(20, 40, FRAME_WIDTH - (MARGIN * 2) - 40, 95, 12, COLORS.prometheusBlack, null, 0, 0.8);
  chatArea.name = "Console_Terminal";
  aiFrame.appendChild(chatArea);
  
  // Terminal prompt text
  const prompt = createText("> AI ready. Type your request...", 35, 60, 12, COLORS.statusGreen, "Medium");
  prompt.name = "Label_Prompt";
  aiFrame.appendChild(prompt);
  
  // Blinking cursor placeholder
  const cursor = createText("█", 35, 85, 12, COLORS.glowYellow, "Regular");
  cursor.name = "Cursor";
  aiFrame.appendChild(cursor);
  
  parent.appendChild(aiFrame);
  return aiFrame;
}

function createGeneratePanel(parent) {
  // Right column (30%) - Spec Template A
  const panelFrame = createFrame("Dashboard/Panel_Generate", FRAME_WIDTH - MARGIN - 280, 105, 260, 580);
  
  // Header - Spec: 18-24px, SemiBold, UPPERCASE
  const header = createText("GENERATE", 0, 0, 20, COLORS.pureWhite, "Bold", 12);
  header.name = "Label_Header";
  header.textAlignHorizontal = "CENTER";
  header.resize(260, 28);
  panelFrame.appendChild(header);
  
  // Generate buttons with 3D glass effect
  const buttons = [
    { label: "COURSE\nPRESENTATION", y: 40, height: 60 },
    { label: "HANDBOOK", y: 110, height: 50 },
    { label: "LESSON PLAN", y: 170, height: 50 },
    { label: "TIMETABLE", y: 230, height: 50 },
    { label: "INSTRUCTOR\nNOTES", y: 290, height: 60 },
    { label: "EXAM", y: 360, height: 50 },
    { label: "INFORMATION\nSHEET", y: 420, height: 60 },
  ];
  
  buttons.forEach(btn => {
    const buttonFrame = createGlassButton(`Btn_${btn.label.replace('\n', '')}`, 15, btn.y, 230, btn.height, btn.label, 20);
    panelFrame.appendChild(buttonFrame);
  });
  
  parent.appendChild(panelFrame);
  return panelFrame;
}

function createBottomStrip(parent) {
  // Spec Section 1.7: Full-width bar
  const statusFrame = createFrame("Global/BottomStrip", MARGIN, FRAME_HEIGHT - 35, FRAME_WIDTH - (MARGIN * 2), 28);
  
  // Subtle background
  const bg = createRoundedRect(0, 0, FRAME_WIDTH - (MARGIN * 2), 28, 4, COLORS.prometheusBlack, COLORS.neonBlue, 1, 0.3);
  bg.name = "Strip_Background";
  statusFrame.appendChild(bg);
  
  // Owner - Spec: Text Soft Grey
  const ownerLabel = createText("OWNER:", 15, 6, 11, COLORS.softGrey, "Regular");
  ownerLabel.name = "Label_Owner";
  statusFrame.appendChild(ownerLabel);
  
  const ownerValue = createText("MATTHEW DODDS", 70, 6, 11, COLORS.statusGreen, "Medium");
  ownerValue.name = "Value_Owner";
  statusFrame.appendChild(ownerValue);
  
  // Start Date
  const startLabel = createText("START DATE:", 200, 6, 11, COLORS.softGrey, "Regular");
  startLabel.name = "Label_StartDate";
  statusFrame.appendChild(startLabel);
  
  const startValue = createText("24/11/25", 285, 6, 11, COLORS.statusGreen, "Medium");
  startValue.name = "Value_StartDate";
  statusFrame.appendChild(startValue);
  
  // Status
  const statusLabel = createText("STATUS:", 380, 6, 11, COLORS.softGrey, "Regular");
  statusLabel.name = "Label_Status";
  statusFrame.appendChild(statusLabel);
  
  const statusValue = createText("IN DEVELOPMENT", 440, 6, 11, COLORS.glowYellow, "Medium");
  statusValue.name = "Value_Status";
  statusFrame.appendChild(statusValue);
  
  // Progress
  const progressLabel = createText("PROGRESS:", 590, 6, 11, COLORS.softGrey, "Regular");
  progressLabel.name = "Label_Progress";
  statusFrame.appendChild(progressLabel);
  
  const progressValue = createText("15%", 665, 6, 11, COLORS.statusGreen, "Medium");
  progressValue.name = "Value_Progress";
  statusFrame.appendChild(progressValue);
  
  // Progress bar background
  const progressBarBg = createRoundedRect(700, 8, 140, 12, 4, COLORS.inactiveGrey, null, 0, 0.4);
  progressBarBg.name = "Progress_Track";
  statusFrame.appendChild(progressBarBg);
  
  // Progress bar fill
  const progressBarFill = createRoundedRect(700, 8, 21, 12, 4, COLORS.statusGreen);
  progressBarFill.name = "Progress_Fill";
  statusFrame.appendChild(progressBarFill);
  
  // Approved status - Spec: Green (#4AFF80) for Approved flag
  const approvedLabel = createText("APPROVED FOR USE:", 1200, 6, 11, COLORS.softGrey, "Regular");
  approvedLabel.name = "Label_Approved";
  statusFrame.appendChild(approvedLabel);
  
  const approvedValue = createText("N", 1340, 6, 11, { r: 0.9, g: 0.2, b: 0.2 }, "Bold");
  approvedValue.name = "Value_Approved";
  statusFrame.appendChild(approvedValue);
  
  parent.appendChild(statusFrame);
  return statusFrame;
}

// Workflow Connectors - Correct flow per spec (Dashboard only)
function createWorkflowConnectors(parent) {
  const connectorsFrame = createFrame("Dashboard/Connectors_Workflow", 0, 0, FRAME_WIDTH, FRAME_HEIGHT);
  connectorsFrame.fills = [];
  
  // Connection points (approximate center positions)
  const courseInfoBottom = { x: 740, y: 305 };
  const courseDescTop = { x: 740, y: 315 };
  const courseDescBottom = { x: 740, y: 515 };
  const courseDescLeft = { x: 460, y: 415 };
  const loRight = { x: 440, y: 415 };
  const nodeRowTop = { x: 740, y: 525 };
  
  // Manager node positions
  const scalarTop = { x: 540, y: 525 };
  const scalarRight = { x: 620, y: 570 };
  const contentLeft = { x: 660, y: 570 };
  const contentRight = { x: 820, y: 570 };
  const lessonLeft = { x: 860, y: 570 };
  
  // C1: Course Information → Course Description (vertical)
  const c1 = createLine(courseInfoBottom.x, courseInfoBottom.y, courseDescTop.x, courseDescTop.y, COLORS.neonBlue, 2, 0.6);
  c1.name = "Connector_C1_Info-Desc";
  connectorsFrame.appendChild(c1);
  
  // C2: Course Description → Learning Objectives (horizontal left)
  const c2 = createLine(courseDescLeft.x, courseDescLeft.y, loRight.x, loRight.y, COLORS.neonBlue, 2, 0.6);
  c2.name = "Connector_C2_Desc-LO";
  connectorsFrame.appendChild(c2);
  
  // C3: Course Description bottom → Node row junction (vertical)
  const c3 = createLine(courseDescBottom.x, courseDescBottom.y, nodeRowTop.x, nodeRowTop.y, COLORS.neonBlue, 2, 0.6);
  c3.name = "Connector_C3_Desc-Nodes";
  connectorsFrame.appendChild(c3);
  
  // Junction node at top of manager row
  const junction = createCircle(nodeRowTop.x - 4, nodeRowTop.y - 4, 8, COLORS.neonBlue);
  junction.name = "Junction_Main";
  addGlowEffect(junction, COLORS.neonBlue, 8, 0.4);
  connectorsFrame.appendChild(junction);
  
  // Branch lines from junction to each manager
  const branchLeft = createLine(nodeRowTop.x, nodeRowTop.y, scalarTop.x, scalarTop.y, COLORS.neonBlue, 2, 0.5);
  branchLeft.name = "Connector_Branch_Scalar";
  connectorsFrame.appendChild(branchLeft);
  
  const branchRight = createLine(nodeRowTop.x, nodeRowTop.y, 940, scalarTop.y, COLORS.neonBlue, 2, 0.5);
  branchRight.name = "Connector_Branch_Lesson";
  connectorsFrame.appendChild(branchRight);
  
  // C5: Scalar → Content (horizontal)
  const c5 = createLine(scalarRight.x, scalarRight.y, contentLeft.x, contentLeft.y, COLORS.neonBlue, 2, 0.5);
  c5.name = "Connector_C5_Scalar-Content";
  connectorsFrame.appendChild(c5);
  
  const junctionSC = createCircle((scalarRight.x + contentLeft.x) / 2 - 3, scalarRight.y - 3, 6, COLORS.neonBlue);
  junctionSC.name = "Junction_SC";
  connectorsFrame.appendChild(junctionSC);
  
  // C6: Content → Lesson (horizontal)
  const c6 = createLine(contentRight.x, contentRight.y, lessonLeft.x, lessonLeft.y, COLORS.neonBlue, 2, 0.5);
  c6.name = "Connector_C6_Content-Lesson";
  connectorsFrame.appendChild(c6);
  
  const junctionCL = createCircle((contentRight.x + lessonLeft.x) / 2 - 3, contentRight.y - 3, 6, COLORS.neonBlue);
  junctionCL.name = "Junction_CL";
  connectorsFrame.appendChild(junctionCL);
  
  parent.appendChild(connectorsFrame);
  return connectorsFrame;
}

// ============================================
// SCALAR MANAGER PAGE
// ============================================

function createScalarControlPanel(parent) {
  // Left column (28-30%) for Scalar Manager
  const leftWidth = 400;
  const panelFrame = createPanel("Scalar/Panel_ScalarControl", MARGIN, 155, leftWidth, 580, "SCALAR CONTROL", COLORS.neonBlue, 28);
  
  // A) IMPORT SCALAR section
  const importBtn = createGlassButton("Btn_ImportScalar", 20, 55, leftWidth - 40, 50, "IMPORT SCALAR", 20);
  panelFrame.appendChild(importBtn);
  
  const importHelp = createText("Import from Excel template (rows 6+, columns B–K).", 25, 115, 10, COLORS.softGrey, "Regular");
  importHelp.name = "Label_ImportHelp";
  panelFrame.appendChild(importHelp);
  
  // B) EDIT TOOLS section
  const editToolsLabel = createText("EDIT TOOLS", 20, 145, 12, COLORS.pureWhite, "SemiBold", 8);
  editToolsLabel.name = "Label_EditTools";
  panelFrame.appendChild(editToolsLabel);
  
  const editTools = ["SELECT", "REORDER", "BULK EDIT", "DELETE"];
  const toolWidth = 80;
  const toolGap = 8;
  editTools.forEach((tool, i) => {
    const toolBtn = createSegmentedButton(`Btn_Tool_${tool}`, 20 + (i * (toolWidth + toolGap)), 165, toolWidth, 28, tool);
    panelFrame.appendChild(toolBtn);
  });
  
  // C) MASTER PKE CONTROL
  const pkeFrame = createFrame("Scalar/PKE_MasterControl", 20, 210, leftWidth - 40, 60);
  
  const pkeBg = createRoundedRect(0, 0, leftWidth - 40, 60, 16, COLORS.prometheusBlack, COLORS.glowYellow, 2, 0.8);
  pkeBg.name = "PKE_Background";
  addGlowEffect(pkeBg, COLORS.glowYellow, 16, 0.3);
  pkeFrame.appendChild(pkeBg);
  
  const pkeIcon = createPKEIcon("Icon_PKE_Master", 15, 15, 28, true);
  pkeFrame.appendChild(pkeIcon);
  
  const pkeLabel = createText("PROMETHEUS: SCALAR BUILDER", 55, 22, 13, COLORS.glowYellow, "SemiBold", 8);
  pkeLabel.name = "Label_PKE";
  pkeFrame.appendChild(pkeLabel);
  
  panelFrame.appendChild(pkeFrame);
  
  // D) NAVIGATION BUTTONS
  const navY = 480;
  const navBtnWidth = (leftWidth - 60) / 2;
  
  const returnBtn = createGlassButton("Btn_ReturnToFront", 20, navY, navBtnWidth, 45, "RETURN TO\nFRONT PAGE", 16);
  panelFrame.appendChild(returnBtn);
  
  const continueBtn = createGlassButton("Btn_ContinueToContent", 30 + navBtnWidth, navY, navBtnWidth, 45, "CONTINUE TO\nCONTENT MGR", 16);
  panelFrame.appendChild(continueBtn);
  
  // Warnings panel
  const warningsPanel = createSmallPanel("Scalar/Panel_Warnings", 20, 290, leftWidth - 40, 170, "WARNINGS", COLORS.neonBlue, 16);
  
  const warningText = createText("No warnings.", 15, 35, 11, COLORS.softGrey, "Regular");
  warningText.name = "Label_WarningContent";
  warningsPanel.appendChild(warningText);
  
  const warningInfo = createText("Bloom's verb validation will appear here.", 15, 55, 10, COLORS.inactiveGrey, "Regular");
  warningInfo.name = "Label_WarningInfo";
  warningsPanel.appendChild(warningInfo);
  
  panelFrame.appendChild(warningsPanel);
  
  parent.appendChild(panelFrame);
  return panelFrame;
}

function createScalarGridPanel(parent) {
  // Right column (70-72%) for Scalar Manager
  const leftColumnWidth = 400 + MARGIN + 20;  // Left panel + margin + gap
  const gridWidth = FRAME_WIDTH - leftColumnWidth - MARGIN;
  const panelFrame = createPanel("Scalar/Panel_ScalarGrid", leftColumnWidth, 155, gridWidth, 580, "COURSE SCALAR", COLORS.neonBlue, 28);
  
  // Column definitions
  const columns = [
    { label: "CLOs", width: 150 },
    { label: "Topics", width: 150 },
    { label: "Subtopics", width: 160 },
    { label: "Lessons", width: 150 },
    { label: "Perf. Criteria", width: 170 },
    { label: "Reserved", width: 140 },
  ];
  
  const columnGap = 8;
  const startX = 20;
  const startY = 50;
  const columnHeight = 510;
  
  let currentX = startX;
  columns.forEach((col, i) => {
    const column = createScalarColumn(
      `Scalar/Column_${col.label.replace(/\s/g, '')}`,
      currentX, startY,
      col.width, columnHeight,
      col.label, 0
    );
    panelFrame.appendChild(column);
    currentX += col.width + columnGap;
  });
  
  parent.appendChild(panelFrame);
  return panelFrame;
}

function createScalarManagerPage() {
  // Create Scalar Manager frame
  const scalarFrame = figma.createFrame();
  scalarFrame.name = "Prometheus V2 – Scalar Manager";
  scalarFrame.resize(FRAME_WIDTH, FRAME_HEIGHT);
  scalarFrame.fills = createSolidPaint(COLORS.prometheusBlack);
  scalarFrame.x = FRAME_WIDTH + 100;  // Position to the right of dashboard
  scalarFrame.y = 0;
  
  // Add subtle radial gradient overlay
  const gradientOverlay = createRoundedRect(FRAME_WIDTH/2 - 400, FRAME_HEIGHT/2 - 300, 800, 600, 400, COLORS.softGrey, null, 0, 0.03);
  gradientOverlay.name = "Background_RadialOverlay";
  scalarFrame.appendChild(gradientOverlay);
  
  // Global elements (same positions as dashboard)
  createHeader(scalarFrame, "SCALAR MANAGER");
  createTopBarButtons(scalarFrame, true);  // LOAD and DELETE disabled
  createStatusInfo(scalarFrame);
  
  // Scalar Manager specific panels
  createScalarControlPanel(scalarFrame);
  createScalarGridPanel(scalarFrame);
  
  // Global elements
  createAIConsole(scalarFrame, 745);
  createBottomStrip(scalarFrame);
  
  return scalarFrame;
}

// ============================================
// DASHBOARD PAGE (Original)
// ============================================

function createDashboardPage() {
  // Create main frame with proper margins
  const mainFrame = figma.createFrame();
  mainFrame.name = "Prometheus_Dashboard_V2";
  mainFrame.resize(FRAME_WIDTH, FRAME_HEIGHT);
  mainFrame.fills = createSolidPaint(COLORS.prometheusBlack);
  
  // Add subtle radial gradient overlay (simulated with rectangle)
  const gradientOverlay = createRoundedRect(FRAME_WIDTH/2 - 400, FRAME_HEIGHT/2 - 300, 800, 600, 400, COLORS.softGrey, null, 0, 0.03);
  gradientOverlay.name = "Background_RadialOverlay";
  mainFrame.appendChild(gradientOverlay);
  
  // Build all UI sections in proper layer order
  createWorkflowConnectors(mainFrame);  // Behind everything
  createHeader(mainFrame);
  createTopBarButtons(mainFrame, false);
  createStatusInfo(mainFrame);
  createCourseSelectionArea(mainFrame);
  createLearningObjectivesPanel(mainFrame);
  createCourseInformationPanel(mainFrame);
  createCourseDescriptionPanel(mainFrame);
  createManagerNodes(mainFrame);
  createAIConsole(mainFrame, 635);
  createGeneratePanel(mainFrame);
  createBottomStrip(mainFrame);
  
  return mainFrame;
}

// ============================================
// MAIN EXECUTION
// ============================================

async function main() {
  try {
    await loadFonts();
    
    // Create Dashboard page
    const dashboardFrame = createDashboardPage();
    
    // Create Scalar Manager page
    const scalarFrame = createScalarManagerPage();
    
    // Center view on the created frames
    figma.viewport.scrollAndZoomIntoView([dashboardFrame, scalarFrame]);
    
    // Select both frames
    figma.currentPage.selection = [dashboardFrame, scalarFrame];
    
    figma.notify("✅ Prometheus V2 Dashboard & Scalar Manager generated!");
    
  } catch (error) {
    figma.notify("❌ Error: " + error.message);
    console.error(error);
  }
  
  figma.closePlugin();
}

main();

// Prometheus Course Generation System 2.0 - Figma UI Generator
// Run this plugin in Figma to generate the complete UI

// ============================================
// COLOR PALETTE
// ============================================
const COLORS = {
  background: { r: 0.035, g: 0.039, b: 0.043 },           // #090A0B - Main background
  panelBg: { r: 0.059, g: 0.067, b: 0.075 },              // #0F1113 - Panel backgrounds
  panelBgDark: { r: 0.039, g: 0.047, b: 0.055 },          // #0A0C0E - Darker panels
  inputBg: { r: 0.078, g: 0.086, b: 0.094 },              // #141618 - Input field backgrounds
  
  cyan: { r: 0.0, g: 0.737, b: 0.831 },                   // #00BCED - Primary cyan accent
  cyanBright: { r: 0.0, g: 0.831, b: 0.918 },             // #00D4EA - Brighter cyan
  cyanDim: { r: 0.0, g: 0.478, b: 0.541 },                // #007A8A - Dimmer cyan for borders
  
  green: { r: 0.0, g: 0.831, b: 0.329 },                  // #00D454 - Green for status values
  greenDark: { r: 0.133, g: 0.38, b: 0.184 },             // #22612F - Dark green for progress
  
  yellow: { r: 0.831, g: 0.678, b: 0.0 },                 // #D4AD00 - Yellow accent (AI window)
  
  white: { r: 1, g: 1, b: 1 },                            // #FFFFFF - White text
  whiteDim: { r: 0.7, g: 0.7, b: 0.7 },                   // #B3B3B3 - Dimmed white text
  
  buttonBg: { r: 0.098, g: 0.106, b: 0.114 },             // #191B1D - Button background
  buttonBorder: { r: 0.2, g: 0.2, b: 0.2 },               // #333333 - Button border
};

// ============================================
// HELPER FUNCTIONS
// ============================================

function rgbToFigma(color) {
  return { r: color.r, g: color.g, b: color.b };
}

function createSolidPaint(color) {
  return [{ type: 'SOLID', color: rgbToFigma(color) }];
}

async function loadFonts() {
  // Load fonts we'll use - using Inter as fallback since it's available in Figma
  await figma.loadFontAsync({ family: "Inter", style: "Regular" });
  await figma.loadFontAsync({ family: "Inter", style: "Medium" });
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

function createRoundedRect(x, y, width, height, cornerRadius, fillColor, strokeColor = null, strokeWeight = 0) {
  const rect = figma.createRectangle();
  rect.x = x;
  rect.y = y;
  rect.resize(width, height);
  rect.cornerRadius = cornerRadius;
  rect.fills = createSolidPaint(fillColor);
  
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
  return frame;
}

function createLine(x1, y1, x2, y2, color, strokeWeight = 1) {
  const line = figma.createLine();
  line.x = x1;
  line.y = y1;
  line.rotation = Math.atan2(y2 - y1, x2 - x1) * (180 / Math.PI);
  const length = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
  line.resize(length, 0);
  line.strokes = createSolidPaint(color);
  line.strokeWeight = strokeWeight;
  return line;
}

// ============================================
// UI COMPONENT BUILDERS
// ============================================

function createButton(name, x, y, width, height, label, cornerRadius = 8) {
  const buttonFrame = createFrame(name, x, y, width, height);
  
  // Button background
  const bg = createRoundedRect(0, 0, width, height, cornerRadius, COLORS.buttonBg, COLORS.buttonBorder, 1);
  bg.name = "Background";
  buttonFrame.appendChild(bg);
  
  // Button label
  const labelText = createText(label, 0, 0, 13, COLORS.white, "Medium", 10);
  labelText.name = "Label";
  labelText.textAlignHorizontal = "CENTER";
  labelText.textAlignVertical = "CENTER";
  labelText.resize(width, height);
  buttonFrame.appendChild(labelText);
  
  return buttonFrame;
}

function createInputField(name, x, y, width, height = 28) {
  const inputFrame = createFrame(name, x, y, width, height);
  
  const bg = createRoundedRect(0, 0, width, height, 4, COLORS.inputBg, COLORS.cyanDim, 1);
  bg.name = "Input Background";
  inputFrame.appendChild(bg);
  
  return inputFrame;
}

function createPanel(name, x, y, width, height, title, strokeColor, cornerRadius = 16) {
  const panelFrame = createFrame(name, x, y, width, height);
  
  // Panel background
  const bg = createRoundedRect(0, 0, width, height, cornerRadius, COLORS.panelBg, strokeColor, 2);
  bg.name = "Panel Background";
  panelFrame.appendChild(bg);
  
  // Panel title
  if (title) {
    const titleText = createText(title, 20, 12, 14, COLORS.white, "Medium", 15);
    titleText.name = "Title";
    panelFrame.appendChild(titleText);
  }
  
  return panelFrame;
}

function createLearningObjectiveItem(index, x, y, width, height) {
  const itemFrame = createFrame(`Objective ${index}`, x, y, width, height);
  
  // Item background
  const bg = createRoundedRect(0, 0, width, height, 8, COLORS.panelBgDark, COLORS.buttonBorder, 1);
  bg.name = "Item Background";
  itemFrame.appendChild(bg);
  
  // Index number
  const indexText = createText(String(index), 10, 8, 12, COLORS.whiteDim, "Regular");
  indexText.name = "Index";
  itemFrame.appendChild(indexText);
  
  // Plus button
  const plusText = createText("+", width - 25, 8, 14, COLORS.whiteDim, "Medium");
  plusText.name = "Add Button";
  itemFrame.appendChild(plusText);
  
  return itemFrame;
}

function createManagerButton(name, x, y, width, height, label) {
  const btnFrame = createFrame(name, x, y, width, height);
  
  // Button background with rounded corners
  const bg = createRoundedRect(0, 0, width, height, 12, COLORS.panelBgDark, COLORS.buttonBorder, 1);
  bg.name = "Background";
  btnFrame.appendChild(bg);
  
  // Split label into lines if needed
  const lines = label.split('\n');
  const lineHeight = 16;
  const startY = (height - (lines.length * lineHeight)) / 2;
  
  lines.forEach((line, i) => {
    const text = createText(line, 0, startY + (i * lineHeight), 13, COLORS.white, "Medium", 10);
    text.name = `Label Line ${i + 1}`;
    text.textAlignHorizontal = "CENTER";
    text.resize(width, lineHeight);
    btnFrame.appendChild(text);
  });
  
  return btnFrame;
}

// ============================================
// MAIN UI SECTIONS
// ============================================

function createHeader(parent) {
  const headerFrame = createFrame("Header", 0, 0, 1456, 70);
  
  // Logo placeholder (flame icon area)
  const logoRect = createRoundedRect(12, 10, 40, 50, 8, COLORS.panelBgDark);
  logoRect.name = "Logo Placeholder";
  headerFrame.appendChild(logoRect);
  
  // Main title
  const title = createText("PROMETHEUS COURSE", 60, 10, 22, COLORS.white, "Bold", 8);
  title.name = "Title Line 1";
  headerFrame.appendChild(title);
  
  const subtitle = createText("GENERATION SYSTEM 2.0", 60, 36, 22, COLORS.white, "Bold", 8);
  subtitle.name = "Title Line 2";
  headerFrame.appendChild(subtitle);
  
  parent.appendChild(headerFrame);
  return headerFrame;
}

function createStatusBar(parent) {
  const statusFrame = createFrame("Status Bar", 12, 68, 420, 70);
  
  // Date/Time
  const dateTime = createText("26/11/25    09:25:43", 0, 0, 11, COLORS.cyan, "Medium");
  dateTime.name = "DateTime";
  statusFrame.appendChild(dateTime);
  
  // Status items
  const statusItems = [
    { label: "Course Loaded:", value: "Example", y: 18 },
    { label: "Duration:", value: "3 Days", y: 30 },
    { label: "Level:", value: "Basic", y: 42 },
    { label: "Thematic:", value: "Intelligence", y: 54 },
  ];
  
  statusItems.forEach(item => {
    const label = createText(item.label, 0, item.y, 11, COLORS.whiteDim, "Regular");
    label.name = `${item.label} Label`;
    statusFrame.appendChild(label);
    
    const value = createText(item.value, 95, item.y, 11, COLORS.green, "Medium");
    value.name = `${item.label} Value`;
    statusFrame.appendChild(value);
  });
  
  parent.appendChild(statusFrame);
  return statusFrame;
}

function createLearningObjectivesPanel(parent) {
  const panelFrame = createPanel("Learning Objectives Panel", 12, 145, 420, 530, null, COLORS.cyan, 20);
  
  // Header
  const header = createText("LEARNING OBJECTIVES", 20, 18, 14, COLORS.white, "Medium", 15);
  header.name = "Header";
  panelFrame.appendChild(header);
  
  // Refresh icon placeholder
  const refreshIcon = createText("↻", 375, 16, 16, COLORS.whiteDim, "Regular");
  refreshIcon.name = "Refresh Icon";
  panelFrame.appendChild(refreshIcon);
  
  // Objective items
  for (let i = 1; i <= 3; i++) {
    const item = createLearningObjectiveItem(i, 15, 50 + ((i - 1) * 100), 385, 90);
    panelFrame.appendChild(item);
  }
  
  // Scrollbar track
  const scrollTrack = createRoundedRect(405, 50, 6, 470, 3, COLORS.panelBgDark);
  scrollTrack.name = "Scroll Track";
  panelFrame.appendChild(scrollTrack);
  
  // Scrollbar thumb
  const scrollThumb = createRoundedRect(405, 50, 6, 150, 3, COLORS.green);
  scrollThumb.name = "Scroll Thumb";
  panelFrame.appendChild(scrollThumb);
  
  parent.appendChild(panelFrame);
  return panelFrame;
}

function createCourseSelectionArea(parent) {
  const selectionFrame = createFrame("Course Selection", 450, 12, 560, 55);
  
  // Label
  const label = createText("SELECT COURSE:", 0, 0, 12, COLORS.whiteDim, "Medium", 10);
  label.name = "Label";
  selectionFrame.appendChild(label);
  
  // Dropdown
  const dropdown = createInputField("Course Dropdown", 0, 22, 560, 32);
  selectionFrame.appendChild(dropdown);
  
  parent.appendChild(selectionFrame);
  return selectionFrame;
}

function createLoadSaveButtons(parent) {
  const buttonsFrame = createFrame("Load Save Buttons", 1180, 12, 260, 40);
  
  const loadBtn = createButton("Load Button", 0, 0, 100, 36, "LOAD", 6);
  buttonsFrame.appendChild(loadBtn);
  
  const saveBtn = createButton("Save Button", 120, 0, 100, 36, "SAVE", 6);
  buttonsFrame.appendChild(saveBtn);
  
  parent.appendChild(buttonsFrame);
  return buttonsFrame;
}

function createCourseInformationPanel(parent) {
  const panelFrame = createPanel("Course Information Panel", 450, 75, 560, 190, null, COLORS.cyan, 12);
  
  // Header with decorative corners
  const header = createText("COURSE INFORMATION", 0, 12, 15, COLORS.cyan, "Medium", 15);
  header.name = "Header";
  header.textAlignHorizontal = "CENTER";
  header.resize(560, 20);
  panelFrame.appendChild(header);
  
  // Form fields
  const fields = [
    { label: "Title:", y: 45 },
    { label: "Level:", y: 75 },
    { label: "Thematic:", y: 105 },
    { label: "Duration:", y: 135, hasCode: true },
    { label: "Developer:", y: 165 },
  ];
  
  fields.forEach(field => {
    const label = createText(field.label, 25, field.y, 12, COLORS.white, "Regular");
    label.name = `${field.label} Label`;
    panelFrame.appendChild(label);
    
    if (field.hasCode) {
      // Duration field is shorter with Code field
      const input = createInputField(`${field.label} Input`, 110, field.y - 4, 180, 26);
      panelFrame.appendChild(input);
      
      const codeLabel = createText("Code:", 310, field.y, 12, COLORS.white, "Regular");
      codeLabel.name = "Code Label";
      panelFrame.appendChild(codeLabel);
      
      const codeInput = createInputField("Code Input", 360, field.y - 4, 180, 26);
      panelFrame.appendChild(codeInput);
    } else {
      const input = createInputField(`${field.label} Input`, 110, field.y - 4, 430, 26);
      panelFrame.appendChild(input);
    }
  });
  
  parent.appendChild(panelFrame);
  return panelFrame;
}

function createCourseDescriptionPanel(parent) {
  const panelFrame = createPanel("Course Description Panel", 450, 275, 560, 220, null, COLORS.cyan, 12);
  
  // Header
  const header = createText("COURSE DESCRIPTION", 0, 12, 14, COLORS.white, "Medium", 15);
  header.name = "Header";
  header.textAlignHorizontal = "CENTER";
  header.resize(560, 20);
  panelFrame.appendChild(header);
  
  // Refresh icon
  const refreshIcon = createText("↻", 520, 10, 14, COLORS.whiteDim, "Regular");
  refreshIcon.name = "Refresh Icon";
  panelFrame.appendChild(refreshIcon);
  
  // Text area background
  const textArea = createRoundedRect(20, 40, 520, 165, 8, COLORS.panelBgDark);
  textArea.name = "Text Area";
  panelFrame.appendChild(textArea);
  
  parent.appendChild(panelFrame);
  return panelFrame;
}

function createManagerButtons(parent) {
  const managersFrame = createFrame("Manager Buttons", 450, 505, 560, 140);
  
  const buttonWidth = 160;
  const buttonHeight = 130;
  const gap = 40;
  
  const managers = [
    { name: "Scalar Manager", label: "SCALAR\nMANAGER", x: 0 },
    { name: "Content Manager", label: "CONTENT\nMANAGER", x: buttonWidth + gap },
    { name: "Lesson Manager", label: "LESSON\nMANAGER", x: (buttonWidth + gap) * 2 },
  ];
  
  managers.forEach(manager => {
    const btn = createManagerButton(manager.name, manager.x, 0, buttonWidth, buttonHeight, manager.label);
    managersFrame.appendChild(btn);
  });
  
  // Connector lines (simplified representation)
  const connectorFrame = createFrame("Connectors", 0, 0, 560, 140);
  connectorFrame.fills = [];
  
  parent.appendChild(managersFrame);
  return managersFrame;
}

function createAIWindow(parent) {
  const aiFrame = createFrame("Prometheus AI Window", 450, 655, 560, 105);
  
  // Background with yellow/gold accent
  const bg = createRoundedRect(0, 0, 560, 105, 8, COLORS.panelBgDark, COLORS.yellow, 2);
  bg.name = "Background";
  aiFrame.appendChild(bg);
  
  // Header
  const header = createText("PROMETHEUS AI", 0, 10, 12, COLORS.whiteDim, "Medium", 10);
  header.name = "Header";
  header.textAlignHorizontal = "CENTER";
  header.resize(560, 16);
  aiFrame.appendChild(header);
  
  // Chat input area
  const chatArea = createRoundedRect(15, 30, 530, 55, 6, COLORS.panelBg);
  chatArea.name = "Chat Area";
  aiFrame.appendChild(chatArea);
  
  // Placeholder text
  const placeholder = createText("AI Chat Text Window here:", 25, 45, 11, COLORS.yellow, "Regular");
  placeholder.name = "Placeholder";
  aiFrame.appendChild(placeholder);
  
  parent.appendChild(aiFrame);
  return aiFrame;
}

function createGeneratePanel(parent) {
  const panelFrame = createFrame("Generate Panel", 1100, 75, 250, 600);
  
  // Header
  const header = createText("GENERATE", 0, 0, 16, COLORS.white, "Bold", 15);
  header.name = "Header";
  header.textAlignHorizontal = "CENTER";
  header.resize(250, 24);
  panelFrame.appendChild(header);
  
  // Generate buttons
  const buttons = [
    { label: "COURSE\nPRESENTATION", y: 35, height: 55 },
    { label: "HANDBOOK", y: 100, height: 45 },
    { label: "LESSON PLAN", y: 155, height: 45 },
    { label: "TIMETABLE", y: 210, height: 45 },
    { label: "INSTRUCTOR\nNOTES", y: 265, height: 55 },
    { label: "EXAM", y: 330, height: 45 },
    { label: "INFORMATION\nSHEET", y: 385, height: 55 },
  ];
  
  buttons.forEach(btn => {
    const buttonFrame = createFrame(btn.label.replace('\n', ' '), 15, btn.y, 220, btn.height);
    
    const bg = createRoundedRect(0, 0, 220, btn.height, 10, COLORS.buttonBg, COLORS.buttonBorder, 1.5);
    bg.name = "Background";
    buttonFrame.appendChild(bg);
    
    const lines = btn.label.split('\n');
    const lineHeight = 16;
    const startY = (btn.height - (lines.length * lineHeight)) / 2;
    
    lines.forEach((line, i) => {
      const text = createText(line, 0, startY + (i * lineHeight), 13, COLORS.white, "Medium", 12);
      text.name = `Label ${i + 1}`;
      text.textAlignHorizontal = "CENTER";
      text.resize(220, lineHeight);
      buttonFrame.appendChild(text);
    });
    
    panelFrame.appendChild(buttonFrame);
  });
  
  parent.appendChild(panelFrame);
  return panelFrame;
}

function createDeleteResetButtons(parent) {
  const buttonsFrame = createFrame("Delete Reset Buttons", 1100, 720, 250, 40);
  
  const deleteBtn = createButton("Delete Button", 0, 0, 100, 36, "DELETE", 6);
  buttonsFrame.appendChild(deleteBtn);
  
  const resetBtn = createButton("Reset Button", 120, 0, 100, 36, "RESET", 6);
  buttonsFrame.appendChild(resetBtn);
  
  parent.appendChild(buttonsFrame);
  return buttonsFrame;
}

function createBottomStatusBar(parent) {
  const statusFrame = createFrame("Bottom Status Bar", 12, 775, 1432, 25);
  
  // Owner
  const ownerLabel = createText("OWNER:", 0, 5, 11, COLORS.whiteDim, "Regular");
  ownerLabel.name = "Owner Label";
  statusFrame.appendChild(ownerLabel);
  
  const ownerValue = createText("MATTHEW DODDS", 50, 5, 11, COLORS.green, "Medium");
  ownerValue.name = "Owner Value";
  statusFrame.appendChild(ownerValue);
  
  // Start Date
  const startLabel = createText("START DATE:", 180, 5, 11, COLORS.whiteDim, "Regular");
  startLabel.name = "Start Date Label";
  statusFrame.appendChild(startLabel);
  
  const startValue = createText("24/11/25", 260, 5, 11, COLORS.green, "Medium");
  startValue.name = "Start Date Value";
  statusFrame.appendChild(startValue);
  
  // Status
  const statusLabel = createText("STATUS:", 340, 5, 11, COLORS.whiteDim, "Regular");
  statusLabel.name = "Status Label";
  statusFrame.appendChild(statusLabel);
  
  const statusValue = createText("IN DEVELOPMENT", 395, 5, 11, COLORS.yellow, "Medium");
  statusValue.name = "Status Value";
  statusFrame.appendChild(statusValue);
  
  // Progress
  const progressLabel = createText("PROGRESS:", 540, 5, 11, COLORS.whiteDim, "Regular");
  progressLabel.name = "Progress Label";
  statusFrame.appendChild(progressLabel);
  
  const progressValue = createText("15%", 610, 5, 11, COLORS.green, "Medium");
  progressValue.name = "Progress Value";
  statusFrame.appendChild(progressValue);
  
  // Progress bar background
  const progressBarBg = createRoundedRect(650, 7, 120, 12, 3, COLORS.panelBgDark);
  progressBarBg.name = "Progress Bar Background";
  statusFrame.appendChild(progressBarBg);
  
  // Progress bar fill
  const progressBarFill = createRoundedRect(650, 7, 18, 12, 3, COLORS.green);
  progressBarFill.name = "Progress Bar Fill";
  statusFrame.appendChild(progressBarFill);
  
  // Approved status
  const approvedLabel = createText("APPROVED FOR USE Y/N:", 1280, 5, 11, COLORS.whiteDim, "Regular");
  approvedLabel.name = "Approved Label";
  statusFrame.appendChild(approvedLabel);
  
  const approvedValue = createText("N", 1420, 5, 11, { r: 0.9, g: 0.2, b: 0.2 }, "Bold");
  approvedValue.name = "Approved Value";
  statusFrame.appendChild(approvedValue);
  
  parent.appendChild(statusFrame);
  return statusFrame;
}

function createConnectorLines(parent) {
  const connectorsFrame = createFrame("Decorative Connectors", 420, 145, 40, 520);
  connectorsFrame.fills = [];
  
  // Vertical line from Learning Objectives to center panel
  const vLine = createLine(20, 100, 20, 400, COLORS.cyanDim, 1);
  vLine.name = "Vertical Connector";
  connectorsFrame.appendChild(vLine);
  
  // Horizontal connector lines
  const hLine1 = createLine(20, 200, 40, 200, COLORS.cyanDim, 1);
  hLine1.name = "H Connector 1";
  connectorsFrame.appendChild(hLine1);
  
  const hLine2 = createLine(20, 350, 40, 350, COLORS.cyanDim, 1);
  hLine2.name = "H Connector 2";
  connectorsFrame.appendChild(hLine2);
  
  parent.appendChild(connectorsFrame);
  return connectorsFrame;
}

// ============================================
// MAIN EXECUTION
// ============================================

async function main() {
  try {
    await loadFonts();
    
    // Create main frame
    const mainFrame = figma.createFrame();
    mainFrame.name = "Prometheus Course Generation System 2.0";
    mainFrame.resize(1456, 810);
    mainFrame.fills = createSolidPaint(COLORS.background);
    
    // Build all UI sections
    createHeader(mainFrame);
    createStatusBar(mainFrame);
    createLearningObjectivesPanel(mainFrame);
    createCourseSelectionArea(mainFrame);
    createLoadSaveButtons(mainFrame);
    createCourseInformationPanel(mainFrame);
    createCourseDescriptionPanel(mainFrame);
    createManagerButtons(mainFrame);
    createAIWindow(mainFrame);
    createGeneratePanel(mainFrame);
    createDeleteResetButtons(mainFrame);
    createBottomStatusBar(mainFrame);
    createConnectorLines(mainFrame);
    
    // Center view on the created frame
    figma.viewport.scrollAndZoomIntoView([mainFrame]);
    
    // Select the main frame
    figma.currentPage.selection = [mainFrame];
    
    figma.notify("✅ Prometheus UI generated successfully!");
    
  } catch (error) {
    figma.notify("❌ Error: " + error.message);
    console.error(error);
  }
  
  figma.closePlugin();
}

main();


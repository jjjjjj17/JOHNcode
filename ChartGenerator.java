import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartFrame;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.CategoryAxis;
import org.jfree.chart.axis.NumberAxis;
import org.jfree.chart.plot.CategoryPlot;
import org.jfree.chart.plot.PiePlot;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.category.DefaultCategoryDataset;
import org.jfree.data.general.DefaultPieDataset;
import org.jfree.chart.renderer.category.BoxAndWhiskerRenderer;
import org.jfree.data.statistics.BoxAndWhiskerCategoryDataset;
import org.jfree.data.statistics.DefaultBoxAndWhiskerCategoryDataset;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.Arrays;
import java.util.HashSet;

public class ChartGenerator extends JFrame implements ActionListener {
    private DefaultCategoryDataset dataset;
    private JTextField dataTextField1;
    private JTextField dataTextField2;
    private JMenuBar menubar;
    private JFileChooser chooser;

    private ChartFrame chartFrame;
    private NextInterface nextInterface;

    public ChartGenerator() {
        dataset = new DefaultCategoryDataset();
        ImageIcon icon = new ImageIcon("C:/test/picpic1.png");
        JLabel coverLabel = new JLabel(icon);
        getContentPane().add(coverLabel, BorderLayout.CENTER);

        JPanel inputPanel1 = new JPanel();
        inputPanel1.add(new JLabel("Data File Path:"));
        dataTextField1 = new JTextField(20);

        inputPanel1.add(dataTextField1);

        JPanel inputPanel2 = new JPanel();
        inputPanel2.add(new JLabel("Data File Path:"));
        dataTextField2 = new JTextField(20);
        inputPanel2.add(dataTextField2);

        JPanel inputPanel = new JPanel(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.gridx = 0;
        gbc.gridy = 0;
        gbc.anchor = GridBagConstraints.WEST;
        gbc.insets = new Insets(5, 5, 5, 5);
        inputPanel.add(inputPanel1, gbc);
        gbc.gridy = 1;
        inputPanel.add(inputPanel2, gbc);

        JButton startButton = new JButton("Start");
        startButton.addActionListener(this);
        inputPanel1.add(startButton);

        getContentPane().add(inputPanel, BorderLayout.NORTH);
        menubar = new JMenuBar();
        setJMenuBar(menubar);

        JMenu fileMenu = new JMenu("File");
        menubar.add(fileMenu);


        JMenuItem openMenuItem = new JMenuItem("Open");
        fileMenu.add(openMenuItem);
        openMenuItem.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent event) {
                chooser = new JFileChooser(".");
                int returnVal = chooser.showOpenDialog(null);
                if (returnVal == JFileChooser.APPROVE_OPTION) {
                    File file = chooser.getSelectedFile();
                    if (dataTextField1.getText().isEmpty()) {
                        dataTextField1.setText(file.getAbsolutePath());
                        dataTextField1.requestFocusInWindow();
                    } else {
                        dataTextField2.setText(file.getAbsolutePath());
                        dataTextField2.requestFocusInWindow();
                    }
                }
            }
        });
        pack();
        setVisible(true);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getActionCommand().equals("Start")) {
            openNextInterface();
        }
    }

    private void openNextInterface() {
        nextInterface = new NextInterface();
        nextInterface.setVisible(true);
    }

    private class NextInterface extends JFrame implements ActionListener {
        private JComboBox<String> chartTypeComboBox;
        private JComboBox<String> xAxisComboBox;
        private JButton inputButton;

        private JButton generateChartButton;

        public NextInterface() {
            setTitle("Next Interface");

            setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
            setSize(800, 600);
            setLocationRelativeTo(null);

            JPanel inputPanel = new JPanel();
            chartTypeComboBox = new JComboBox<>();
            chartTypeComboBox.addItem("Line Chart");
            chartTypeComboBox.addItem("Bar Chart");
            chartTypeComboBox.addItem("Pie Chart");
            chartTypeComboBox.addItem("Venn Diagram");
            chartTypeComboBox.addItem("Box plot");
            inputPanel.add(new JLabel("Chart Type:"));
            inputPanel.add(chartTypeComboBox);

            inputButton = new JButton("Enter");
            inputButton.addActionListener(this);

            inputPanel.add(inputButton);

            String imagePath = "C:/test/picpic.png";
            ImageIcon icon = new ImageIcon(imagePath);
            JLabel coverLabel = new JLabel(icon);
            getContentPane().add(coverLabel, BorderLayout.CENTER);


            generateChartButton = new JButton("Generate Chart");
            generateChartButton.addActionListener(this);
            inputPanel.add(generateChartButton);

            getContentPane().add(inputPanel, BorderLayout.NORTH);
        }

        @Override
        public void actionPerformed(ActionEvent e) {
            if (e.getSource() == inputButton) {
                selectAxes();
            } else if (e.getSource() == generateChartButton) {
                generateChart();
            }
        }

        private void selectAxes() {
            inputButton.setVisible(false);
            generateChartButton.setVisible(true);
            chartTypeComboBox.setEnabled(false);

            String dataFilePath = dataTextField1.getText();

            loadDataFromFile(dataFilePath);
        }

        private void generateChart() {
            String chartType = (String) chartTypeComboBox.getSelectedItem();
            String file1Path = dataTextField1.getText();
            String file2Path = dataTextField2.getText();
            String filePath1 = dataTextField1.getText();
            String filePath2 = dataTextField2.getText();
            HashSet<String> file1Data = readFileData(file1Path);
            HashSet<String> file2Data = readFileData(file2Path);
            HashSet<String> fileData1 = readFileData(filePath1);
            HashSet<String> fileData2 = readFileData(filePath2);
            DefaultBoxAndWhiskerCategoryDataset boxPlotDataset = createBoxPlotDataset();

            HashSet<String> commonData = new HashSet<>(file1Data);
            commonData.retainAll(file2Data);

            JFreeChart chart = null;
            if (chartType.equals("Line Chart")) {
                chart = ChartFactory.createLineChart("Line Chart", "Category", "Value", dataset, PlotOrientation.VERTICAL, true, true, false);
            } else if (chartType.equals("Bar Chart")) {
                chart = ChartFactory.createBarChart("Bar Chart", "Category", "Value", dataset, PlotOrientation.VERTICAL, true, true, false);
            } else if (chartType.equals("Pie Chart")) {
                chart = createPieChart("Pie Chart", dataset);
            } else if (chartType.equals("Venn Diagram")) {
                drawVennDiagram(file1Data.size(), file2Data.size(), commonData.size());
            } else if (chartType.equals("Box plot")) {
                chart = createBoxPlot("Box Plot", boxPlotDataset);
            }

            if (chartFrame == null) {
                chartFrame = new ChartFrame("Chart", chart);
                chartFrame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
            } else {
                chartFrame.dispose();
                chartFrame = new ChartFrame("Chart", chart);
                chartFrame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
            }
            chartFrame.setSize(800, 600);
            chartFrame.setVisible(true);

        }
        private DefaultBoxAndWhiskerCategoryDataset createBoxPlotDataset() {
            DefaultBoxAndWhiskerCategoryDataset dataset = new DefaultBoxAndWhiskerCategoryDataset();

            // 將範例資料添加到資料集
            dataset.add(Arrays.asList(1.0, 2.0, 3.0, 4.0, 5.0), "Category 1", "Value 1");
            dataset.add(Arrays.asList(1.0, 2.0, 3.0, 4.0, 5.0), "Category 2", "Value 2");


            return dataset;
        }
        private HashSet<String> readFileData(String filePath) {
            HashSet<String> data = new HashSet<>();
            try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
                String line;
                boolean isFirstLine = true;
                while ((line = reader.readLine()) != null) {
                    if (isFirstLine) {
                        isFirstLine = false;
                        continue; // Skip the first line (title)
                    }
                    String[] values = line.split("\\t"); // Assuming tab-separated values
                    if (values.length > 0) {
                        data.add(values[0]);
                    }
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
            return data;
        }

        private void loadDataFromFile(String filePath) {
            dataset.clear();

            double minYValue = Double.POSITIVE_INFINITY;
            double maxYValue = Double.NEGATIVE_INFINITY;

            try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
                String line;
                int rowNumber = 0;
                String[] headers = null;

                while ((line = br.readLine()) != null) {
                    String[] data = line.split("\t");


                    // Get the row label (month)

                    if (rowNumber == 0) {
                        headers = Arrays.copyOfRange(data, 1, data.length);  // Skip the first element (0,0)
                    } else {
                        String rowLabel = data[0];

                        for (int columnIndex = 1; columnIndex < data.length; columnIndex++) {
                            double value = Double.parseDouble(data[columnIndex]);
                            String category = headers[columnIndex - 1];
                            dataset.addValue(value, category, rowLabel);
                            minYValue = Math.min(minYValue, value);
                            maxYValue = Math.max(maxYValue, value);
                        }
                    }

                    rowNumber++;
                }
            } catch (IOException e) {
                e.printStackTrace();
            }

            // Check if the range is too small
            if (minYValue == maxYValue) {
                double rangePadding = Math.abs(minYValue) * 0.1; // Add 10% padding to the range
                minYValue -= rangePadding;
                maxYValue += rangePadding;
            }

            NumberAxis yAxis = new NumberAxis("Value");
            double rangePadding = (maxYValue - minYValue) * 0.1; // Add 10% padding to the range
            yAxis.setRangeWithMargins(minYValue - rangePadding, maxYValue + rangePadding);


        }

        private JFreeChart createPieChart(String title, DefaultCategoryDataset dataset) {
            DefaultPieDataset pieDataset = new DefaultPieDataset();

            try (BufferedReader br = new BufferedReader(new FileReader(dataTextField1.getText()))) {
                String line;
                int rowNumber = 0;
                String[] categories = null;
                boolean isFirstLine = true;

                while ((line = br.readLine()) != null) {
                    String[] data = line.split("\t");

                    if (rowNumber > 0) {
                        String rowLabel = data[0];
                        for (int columnIndex = 1; columnIndex < data.length; columnIndex++) {
                            if (columnIndex == 0) {
                                continue;
                            }
                            double value = Double.parseDouble(data[columnIndex]);
                            String category = categories[columnIndex - 1];

                            pieDataset.setValue(category, value);
                        }
                    } else {
                        categories = Arrays.copyOfRange(data, 1, data.length); // Skip the first element in each row
                    }

                    rowNumber++;
                }
            } catch (IOException e) {
                e.printStackTrace();
            }

            JFreeChart chart = ChartFactory.createPieChart(title, pieDataset, true, true, false);

            return chart;
        }

        private JFreeChart createBoxPlot(String title, BoxAndWhiskerCategoryDataset dataset) {
            JFreeChart chart = ChartFactory.createBoxAndWhiskerChart(
                    title, "Category", "Value", dataset, true);
            CategoryPlot plot = (CategoryPlot) chart.getPlot();
            BoxAndWhiskerRenderer renderer = new BoxAndWhiskerRenderer();
            plot.setRenderer(renderer);
            CategoryAxis domainAxis = plot.getDomainAxis();
            domainAxis.setCategoryMargin(0.1); // 設定分類之間的間距
            domainAxis.setUpperMargin(0.2); // 調整上邊距以留空間給分類標籤
            domainAxis.setLowerMargin(0.2); // 調整下邊距以留空間給分類標籤
            domainAxis.setCategoryLabelPositionOffset(15); // 調整分類標籤的位移量
            return chart;
        }
    }

    private void drawVennDiagram(int set1Size, int set2Size, int commonSize) {
        DefaultPieDataset dataset = new DefaultPieDataset();
        dataset.setValue("Set 1 Only", set1Size - commonSize);
        dataset.setValue("Set 2 Only", set2Size - commonSize);
        dataset.setValue("Common", commonSize);

        JFreeChart chart = ChartFactory.createPieChart("Venn Diagram", dataset, true, true, false);

        PiePlot plot = (PiePlot) chart.getPlot();
        plot.setSectionOutlinesVisible(false);
        plot.setLabelGenerator(null);

        ChartFrame frame = new ChartFrame("Venn Diagram", chart);
        frame.pack();
        frame.setVisible(true);
    }

    public static void main(String[] args) {
        new ChartGenerator1();
        String imagePath = "C:/test/picpic.png";

    }
}


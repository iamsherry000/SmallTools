import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

/**
 * SimpleTimer — a tiny Java Swing countdown timer.
 * UX:
 *  - Orange/white theme
 *  - Set hours/minutes/seconds, click "開始" (bottom-right) to start
 *  - When time is up, shows a dialog "時間到！"
 */
public class TimerApp {
    private JFrame frame;
    private JSpinner hSpinner, mSpinner, sSpinner;
    private JButton startBtn, stopBtn, resetBtn;
    private JLabel countdownLabel;
    private javax.swing.Timer swingTimer;
    private int remainingSeconds = 0;

    // Theme colors
    private static final Color ORANGE = new Color(0xFF8C00); // dark orange
    private static final Color SOFT_ORANGE = new Color(0xFFE8CC);
    private static final Font COUNTDOWN_FONT = new Font("Segoe UI", Font.BOLD, 48);

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new TimerApp().createAndShow());
    }

    private void createAndShow() {
        frame = new JFrame("SimpleTimer");
        frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        frame.setSize(420, 240);
        frame.setLocationRelativeTo(null);
        frame.setLayout(new BorderLayout(12, 12));

        // Top title bar
        JLabel title = new JLabel("⏱️ 倒數計時器", SwingConstants.LEFT);
        title.setBorder(BorderFactory.createEmptyBorder(12, 12, 0, 12));
        title.setForeground(ORANGE);
        title.setFont(new Font("Segoe UI", Font.BOLD, 20));
        frame.add(title, BorderLayout.NORTH);

        // Center panel: spinners + big countdown label
        JPanel center = new JPanel(new GridBagLayout());
        center.setBackground(Color.WHITE);
        GridBagConstraints gc = new GridBagConstraints();
        gc.insets = new Insets(6, 6, 6, 6);
        gc.gridx = 0; gc.gridy = 0; gc.anchor = GridBagConstraints.LINE_END;
        center.add(new JLabel("小時:"), gc);
        gc.gridx = 1; gc.anchor = GridBagConstraints.LINE_START;
        hSpinner = makeSpinner(0, 0, 99);
        center.add(hSpinner, gc);

        gc.gridx = 2; gc.anchor = GridBagConstraints.LINE_END;
        center.add(new JLabel("分鐘:"), gc);
        gc.gridx = 3; gc.anchor = GridBagConstraints.LINE_START;
        mSpinner = makeSpinner(0, 0, 59);
        center.add(mSpinner, gc);

        gc.gridx = 4; gc.anchor = GridBagConstraints.LINE_END;
        center.add(new JLabel("秒:"), gc);
        gc.gridx = 5; gc.anchor = GridBagConstraints.LINE_START;
        sSpinner = makeSpinner(0, 0, 59);
        center.add(sSpinner, gc);

        // Big label row
        gc.gridx = 0; gc.gridy = 1; gc.gridwidth = 6; gc.fill = GridBagConstraints.HORIZONTAL;
        countdownLabel = new JLabel("00:00:00", SwingConstants.CENTER);
        countdownLabel.setFont(COUNTDOWN_FONT);
        countdownLabel.setOpaque(true);
        countdownLabel.setBackground(SOFT_ORANGE);
        countdownLabel.setForeground(Color.DARK_GRAY);
        countdownLabel.setBorder(BorderFactory.createEmptyBorder(12, 12, 12, 12));
        center.add(countdownLabel, gc);

        frame.add(center, BorderLayout.CENTER);

        // Bottom action bar (start at bottom-right)
        JPanel actions = new JPanel(new FlowLayout(FlowLayout.RIGHT, 12, 12));
        actions.setBackground(Color.WHITE);
        startBtn = makeButton("開始", ORANGE, Color.WHITE);
        stopBtn = makeButton("停止", new Color(0xDD4444), Color.WHITE);
        resetBtn = makeButton("重置", new Color(0x666666), Color.WHITE);
        stopBtn.setEnabled(false);
        resetBtn.setEnabled(false);

        actions.add(resetBtn);
        actions.add(stopBtn);
        actions.add(startBtn); // last => visually bottom-right
        frame.add(actions, BorderLayout.SOUTH);

        // Timer logic: tick every 1 sec
        swingTimer = new javax.swing.Timer(1000, e -> onTick());

        startBtn.addActionListener(e -> onStart());
        stopBtn.addActionListener(e -> onStop());
        resetBtn.addActionListener(e -> onReset());

        // Accents around root
        frame.getRootPane().setBorder(BorderFactory.createMatteBorder(6, 0, 0, 0, ORANGE));
        frame.getContentPane().setBackground(Color.WHITE);
        frame.setVisible(true);
    }

    private JSpinner makeSpinner(int value, int min, int max) {
        SpinnerNumberModel model = new SpinnerNumberModel(value, min, max, 1);
        JSpinner sp = new JSpinner(model);
        sp.setPreferredSize(new Dimension(64, 28));
        ((JSpinner.DefaultEditor) sp.getEditor()).getTextField().setColumns(2);
        return sp;
    }

    private JButton makeButton(String text, Color bg, Color fg) {
        JButton b = new JButton(text);
        b.setBackground(bg);
        b.setForeground(fg);
        b.setFocusPainted(false);
        b.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(bg.darker()),
                BorderFactory.createEmptyBorder(6, 14, 6, 14)));
        b.addMouseListener(new java.awt.event.MouseAdapter() {
            @Override public void mouseEntered(MouseEvent e) { b.setBackground(bg.brighter()); }
            @Override public void mouseExited(MouseEvent e) { b.setBackground(bg); }
        });
        return b;
    }

    private void onStart() {
        int h = (int) hSpinner.getValue();
        int m = (int) mSpinner.getValue();
        int s = (int) sSpinner.getValue();
        remainingSeconds = h * 3600 + m * 60 + s;

        if (remainingSeconds <= 0) {
            JOptionPane.showMessageDialog(frame, "請設定一個大於 0 的時間。", "提醒", JOptionPane.INFORMATION_MESSAGE);
            return;
        }
        updateCountdownLabel();
        setInputsEnabled(false);
        swingTimer.start();
    }

    private void onStop() {
        swingTimer.stop();
        setInputsEnabled(true);
    }

    private void onReset() {
        swingTimer.stop();
        remainingSeconds = 0;
        countdownLabel.setText("00:00:00");
        setInputsEnabled(true);
    }

    private void onTick() {
        remainingSeconds--;
        updateCountdownLabel();
        if (remainingSeconds <= 0) {
            swingTimer.stop();
            setInputsEnabled(true);
            Toolkit.getDefaultToolkit().beep();
            JOptionPane.showMessageDialog(frame, "時間到！", "提醒", JOptionPane.INFORMATION_MESSAGE);
        }
    }

    private void updateCountdownLabel() {
        int h = Math.max(0, remainingSeconds) / 3600;
        int m = (Math.max(0, remainingSeconds) % 3600) / 60;
        int s = Math.max(0, remainingSeconds) % 60;
        countdownLabel.setText(String.format("%02d:%02d:%02d", h, m, s));
    }

    private void setInputsEnabled(boolean enabled) {
        hSpinner.setEnabled(enabled);
        mSpinner.setEnabled(enabled);
        sSpinner.setEnabled(enabled);
        startBtn.setEnabled(enabled);
        stopBtn.setEnabled(!enabled);
        resetBtn.setEnabled(!enabled);
    }
}

/* =========================
 * Build & Package (Windows)
 * =========================
 * 1) Compile & make runnable JAR (JDK 11+):
 *    javac TimerApp.java
 *    jar cfe SimpleTimer.jar TimerApp TimerApp.class
 *
 * 2A) Create .exe with jpackage (JDK 17+ has it):
 *    jpackage --type exe --name SimpleTimer \
 *      --input . --main-jar SimpleTimer.jar --main-class TimerApp \
 *      --win-shortcut --win-menu
 *    => outputs SimpleTimer-1.0.exe (name can vary by JDK)
 *
 * 2B) Or use Launch4j (GUI tool):
 *    - Download Launch4j
 *    - Set "Output file" to something like C:\\path\\SimpleTimer.exe
 *    - Set "Jar" to your SimpleTimer.jar
 *    - (Optional) Set JRE min version (e.g., 11)
 *    - Build wrapper => produces SimpleTimer.exe
 *
 * Notes:
 *  - If you want an icon, add: --icon path\\to\\icon.ico (jpackage), or set in Launch4j.
 *  - For a self-contained exe (bundled JRE), add to jpackage:
 *      --runtime-image <path-to-custom-jre>  (or let jpackage create one with --strip-native-commands)
 */

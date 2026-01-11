from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.lang import Builder
from kivy.factory import Factory
from script.math import calcCreator, wordQuestionCreator
from script.social import SocialQuestionCreator
from script.science import ScienceQuestionCreator
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.metrics import dp

PRIMARY_COLOR = get_color_from_hex("#c1d1e0")
ACCENT_COLOR = get_color_from_hex("#FF6B6B")

# キーボード表示時に画面を上にずらす
Window.softinput_mode = 'below_target'

# kvファイルを読み込む
# ShikakuAppの名前から自動的にshikaku.kvが読み込まれるため不要

# --------------------
# 各モードの画面
# --------------------

# スプラッシュ画面
class SplashScreen(Screen):
    pass

# メイン画面（モード選択）
# メイン画面（モード選択）
class MainScreen(Screen):
    pass

# --------------------
# 算数モード
# --------------------
class MathCalcScreen(Screen):
    question_text = StringProperty("")
    result_text = StringProperty("")
    button_text = StringProperty("けってい")
    is_correct = False  # 正解したかどうかのフラグ
    params = None # 問題生成クラスのインスタンス
    RESULT_FONT_SIZE = dp(48)
    HEADER_FONT_SIZE = dp(24)

    def on_pre_enter(self):
        # 画面が表示される直前に新しい問題を作る
        self.create_question()

    def on_button_press(self, answer_input):
        """ボタンが押された時の処理（2段階）"""
        if not self.is_correct:
            # 第1段階：答えをチェック
            self.check_answer(answer_input.text)
        else:
            # 第2段階：次の問題へ
            self.next_question(answer_input)

    def check_answer(self, ans):
        if self.params is None: return

        try:
            # 正解は shikaku_value (隠されている数字)
            correct_val = self.params.shikaku_value

            if int(ans) == correct_val:
                common.add_reward("math", 1)
                self.ids.header_label.text = "せいかい！！ ◎"
                self.ids.header_label.color = ACCENT_COLOR
                self.ids.header_label.bold = True
                self.ids.header_label.font_size = self.RESULT_FONT_SIZE
                self.button_text = "次へ"
                self.is_correct = True
            else:
                self.ids.header_label.text = "ちがうよ"
                self.ids.header_label.color = ACCENT_COLOR
                self.ids.header_label.bold = True
                self.ids.header_label.font_size = self.RESULT_FONT_SIZE
        except Exception as e:
            self.ids.header_label.text = "数字をいれてね"
            self.ids.header_label.color = ACCENT_COLOR
            self.ids.header_label.bold = True
            self.ids.header_label.font_size = self.RESULT_FONT_SIZE

    def next_question(self, answer_input):
        """次の問題を表示"""
        self.is_correct = False
        self.button_text = "けってい"
        self.ids.header_label.text = "もんだい"
        self.ids.header_label.color = PRIMARY_COLOR
        self.ids.header_label.bold = False
        self.ids.header_label.font_size = self.HEADER_FONT_SIZE
        answer_input.text = ""
        self.create_question()

    def create_question(self):
        """新しい問題を作る"""
        self.params = calcCreator()
        result_dict = self.params.main()
        
        # 辞書から数式文字列を取得して表示
        # calcCreator側ですでに [ ] に置換済みなので、そのまま表示すればOK
        self.question_text = result_dict["formula_str"]
            
class MathTextScreen(Screen):
    question_text = StringProperty("文章題サンプル")
    result_text = StringProperty("")
    button_text = StringProperty("けってい")
    is_correct = False
    params = None

    def on_pre_enter(self):
        self.create_question()

    def on_button_press(self, answer_input):
        if not self.is_correct:
            self.check_answer(answer_input.text)
        else:
            self.next_question(answer_input)

    def check_answer(self, ans):
        if self.params is None: return

        try:
            correct_val = self.params.get("shikaku_value")
            
            if int(ans) == correct_val:
                common.add_reward("math", 1)
                self.ids.header_label.text = "せいかい！！ ◎"
                self.ids.header_label.color = ACCENT_COLOR
                self.ids.header_label.bold = True
                self.ids.header_label.font_size = dp(48)
                self.button_text = "次へ"
                self.is_correct = True
            else:
                self.ids.header_label.text = "ちがうよ"
                self.ids.header_label.color = ACCENT_COLOR
                self.ids.header_label.bold = True
                self.ids.header_label.font_size = dp(48)
        except Exception as e:
            self.ids.header_label.text = "数字をいれてね"
            self.ids.header_label.color = ACCENT_COLOR
            self.ids.header_label.bold = True
            self.ids.header_label.font_size = 48

    def next_question(self, answer_input):
        self.is_correct = False
        self.button_text = "けってい"
        self.ids.header_label.text = "もんだい"
        self.ids.header_label.color = PRIMARY_COLOR
        self.ids.header_label.bold = False
        self.ids.header_label.font_size = dp(24)
        answer_input.text = ""
        self.create_question()

    def create_question(self):
        creator = wordQuestionCreator()
        self.params = creator.main()
        self.question_text = self.params["formula_str"]
        self.result_text = ""

class MathScreen(Screen):
    def on_pre_enter(self):
        # 画面遷移時に現在表示中の画面のcreate_questionを呼び出す
        if "math_inner" in self.ids:
            current_screen = self.ids.math_inner.current_screen
            if hasattr(current_screen, "create_question"):
                current_screen.create_question()

# --------------------
# 社会モード
# --------------------
class SocialQAScreen(Screen):
    question_text   = StringProperty("一問一答サンプル")
    result_text     = StringProperty("")
    button_text     = StringProperty("けってい")
    choices_text    = StringProperty("")
    is_correct      = False
    params          = None

    def on_pre_enter(self):
        self.create_question()

    def on_button_press(self, answer_input):
        if not self.is_correct:
            self.check_answer(answer_input.text)
        else:
            self.next_question(answer_input)

    def check_answer(self, ans):
        if self.params is None: return

        try:
            correct_val = self.params.get("answer")
            # Remove spaces from answer just in case
            if ans.strip() == correct_val:
                common.add_reward("social", 1)
                self.ids.header_label.text = "せいかい！！ ◎"
                self.ids.header_label.color = ACCENT_COLOR
                self.ids.header_label.bold = True
                self.ids.header_label.font_size = dp(48)
                self.button_text = "次へ"
                self.is_correct = True
            else:
                self.ids.header_label.text = "！！ちがうよ！！"
                self.ids.header_label.color = ACCENT_COLOR
                self.ids.header_label.bold = True
                self.ids.header_label.font_size = dp(48)
        except Exception as e:
            self.ids.header_label.text = "文字をいれてね"
            self.ids.header_label.color = ACCENT_COLOR
            self.ids.header_label.bold = True
            self.ids.header_label.font_size = 48

    def next_question(self, answer_input):
        self.is_correct = False
        self.button_text = "けってい"
        self.ids.header_label.text = "もんだい"
        self.ids.header_label.color = PRIMARY_COLOR
        self.ids.header_label.bold = False
        answer_input.text = ""
        self.create_question()

    def create_question(self):
        creator = SocialQuestionCreator()
        self.params = creator.main()
        self.question_text = self.params["question"]
        
        # Format choices
        choices = self.params.get("choices", [])
        self.choices_text = " / ".join(choices)
        self.result_text = ""


class SocialScreen(Screen):
    def on_pre_enter(self):
        if "social_inner" in self.ids:
            current_screen = self.ids.social_inner.current_screen
            if hasattr(current_screen, "create_question"):
                current_screen.create_question()

# --------------------
# 理科モード
# --------------------
class ScienceQAScreen(Screen):
    question_text = StringProperty("一問一答サンプル")
    result_text = StringProperty("")
    button_text = StringProperty("けってい")
    choices_text = StringProperty("")
    is_correct = False
    params = None

    def on_pre_enter(self):
        self.create_question()

    def on_button_press(self, answer_input):
        if not self.is_correct:
            self.check_answer(answer_input.text)
        else:
            self.next_question(answer_input)

    def check_answer(self, ans):
        if self.params is None: return

        try:
            correct_val = self.params.get("answer")
            if ans.strip() == correct_val:
                common.add_reward("science", 1)
                self.ids.header_label.text = "せいかい！！ ◎"
                self.ids.header_label.color = ACCENT_COLOR
                self.ids.header_label.bold = True
                self.ids.header_label.font_size = dp(48)
                self.button_text = "次へ"
                self.is_correct = True
            else:
                self.ids.header_label.text = "ちがうよ"
                self.ids.header_label.color = ACCENT_COLOR
                self.ids.header_label.bold = True
                self.ids.header_label.font_size = dp(48)
        except Exception as e:
            self.ids.header_label.text = "文字をいれてね"
            self.ids.header_label.color = ACCENT_COLOR
            self.ids.header_label.bold = True
            self.ids.header_label.font_size = dp(48)

    def next_question(self, answer_input):
        self.is_correct = False
        self.button_text = "けってい"
        self.ids.header_label.text = "もんだい"
        self.ids.header_label.color = PRIMARY_COLOR
        self.ids.header_label.bold = False
        answer_input.text = ""
        self.create_question()

    def create_question(self):
        creator = ScienceQuestionCreator()
        self.params = creator.main()
        self.question_text = self.params["question"]
        choices = self.params.get("choices", [])
        self.choices_text = " / ".join(choices)
        self.result_text = ""


class ScienceScreen(Screen):
    def on_pre_enter(self):
        if "science_inner" in self.ids:
            current_screen = self.ids.science_inner.current_screen
            if hasattr(current_screen, "create_question"):
                current_screen.create_question()

# --------------------
# ポイント画面 (RewardScreen)
# --------------------
from script import common


class RewardScreen(Screen):
    total_point = StringProperty("0")
    math_point = StringProperty("0")
    social_point = StringProperty("0")
    science_point = StringProperty("0")

    def on_enter(self, *args):
        # 画面に入ったら rewards.json から読み込む
        rewards = common.get_rewards()
        if rewards:
            # 辞書から値を取得して反映（キーがなければ0）
            self.total_point = str(rewards.get("total", 0))
            self.math_point = str(rewards.get("math", 0))
            self.social_point = str(rewards.get("social", 0))
            self.science_point = str(rewards.get("science", 0))

    def confirm_reset(self):
        Factory.ResetConfirmPopup(target_screen=self).open()

    def do_reset(self):
        common.reset_rewards()
        self.on_enter()

class ResetConfirmPopup(Popup):
    target_screen = ObjectProperty(None)

# --------------------
# 設定画面 (SettingsScreen)
# --------------------
class SettingsScreen(Screen):
    difficulty_value = NumericProperty(1)
    difficulty_text = StringProperty("1")
    username_text = StringProperty("ゲスト")

    def on_enter(self, *args):
        # 画面に入ったら settings.json から読み込む
        diff = common.get_settings("difficulty")
        if diff is not None:
            self.difficulty_value = diff
            self.difficulty_text = str(diff)
        
        name = common.get_settings("username")
        if name:
            self.username_text = name
        else:
            self.username_text = "ゲスト"

    def on_value_change(self, instance, value):
        # スライダーの値が変わったら呼ばれる
        val = int(value)
        self.difficulty_value = val
        self.difficulty_text = str(val)

    def save_settings(self):
        # 設定を保存する
        common.set_setting("difficulty", int(self.difficulty_value))

    def open_username_popup(self):
        popup = UserNamePopup()
        popup.bind(on_dismiss=self.update_username)
        popup.open()

    def update_username(self, instance):
        name = common.get_settings("username")
        if name:
            self.username_text = name

# --------------------
# ルートのScreenManager
# --------------------
class UserNamePopup(Popup):
    input_text = ObjectProperty(None)
    
    def save_name(self):
        name = self.input_text.text.strip()
        if name:
            common.set_setting("username", name)
            self.dismiss()

# --------------------
# ルートのScreenManager
# --------------------
class RootWidget(ScreenManager):
    pass

# --------------------
# App
# --------------------
class ShikakuApp(App):
    def build(self):
        return RootWidget()

    def on_start(self):
        # ユーザー名が設定されているか確認
        username = common.get_settings("username")
        if username is None:
            # ユーザー名未設定ならポップアップを表示
            # Clock.schedule_once を使って描画後に表示する
            Clock.schedule_once(lambda dt: self.show_username_popup(), 0.5)
            
    def show_username_popup(self):
        UserNamePopup().open()


if __name__ == "__main__":
    ShikakuApp().run()

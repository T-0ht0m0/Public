import PySimpleGUI as sg
import pathlib
import subprocess as sp


def get_tex_files(path):
    # texファイルパスの取得
    tex_list0 = path.glob("**/*.tex")
    list = []
    tex_list = []
    for tex_file in tex_list0:
        cmd = sp.Popen(["nkf", "-g", tex_file], stdout=sp.PIPE)
        encoding = cmd.stdout.readlines()
        folder_name = tex_file.parent
        file_name = tex_file.name
        #print(type(folder_name),type(file_name))
        list.append(
            [folder_name, file_name, str(*encoding).lstrip("b").replace("\\n", "")]
        )
        tex_list.append(tex_file)
    return tex_list, list


if __name__ == '__main__':

    home_path = pathlib.Path.home() / "Desktop"

    # フォルダパスの取得
    path_folder = sg.popup_get_folder(
        "変換したいTeXファイルが入っているフォルダを選択してください",
        title=None,
        default_path=home_path,
        font="Helvetica 14",
        initial_folder=home_path,
    )
    path = pathlib.Path(path_folder)
    tex_list, list = get_tex_files(path)
    #print(tex_list)
    #print(list)

    H = ["場所", "TeX file", "文字コード"]

    layout = [
        [sg.Button("フォルダ選択", key="select")],
        [
            sg.Table(
                list,
                headings=H,
                auto_size_columns=False,
                vertical_scroll_only=False,
                def_col_width=20,
                num_rows=20,
                display_row_numbers=True,
                header_text_color="#0000ff",
                header_background_color="#cccccc",
                key="table",
                # font="Helvetica 20",
                justification="left",
            )
        ],
        [
            sg.Button("Quit"),
            sg.Button("Shift-JISに変更", key="sjis"),
            sg.Button("UTF-8に変更", key="utf8"),
        ],
    ]

    window = sg.Window("utf8 shift-jis", layout, font="Helvetica 14")

    while True:
        event, values = window.read()  # イベントの読み取り(イベント待ち)
        if event in (None, "Quit"):
            # print("終了します.")
            break  # 終了処理

        elif event == "select":
            # フォルダパスの取得
            temp_path_folder = path_folder
            path_folder = sg.popup_get_folder(
                "変換したいTeXファイルが入っているフォルダを選択してください",
                title=None,
                default_path=home_path,
                font="Helvetica 14",
                initial_folder=home_path,
            )
            if path_folder is None:
                path_folder = temp_path_folder
            path = pathlib.Path(path_folder)
            tex_list, list = get_tex_files(path)
            window["table"].update(list)

        elif event == "sjis":
            # print("s-jis")
            for tex in tex_list:
                sp.Popen(["nkf", "-s", "--overwrite", tex])
            tex_list, list = get_tex_files(path)
            window["table"].update(list)

        elif event == "utf8":
            # print("utf-8")
            for tex in tex_list:
                sp.Popen(["nkf", "-w", "--overwrite", tex])
            tex_list, list = get_tex_files(path)
            window["table"].update(list)

    window.close()

    # 終了条件(None:クローズボタン)

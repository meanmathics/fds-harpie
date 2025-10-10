import streamlit as st
import pandas as pd

def aplicar_estilo_customizado():
    st.markdown("""
        <style>
            [data-testid="stSidebar"], [data-testid="stHeader"] {
                display: none;
            }

            .main {
                z-index: 1;
            }

            .stApp, div[data-testid="stAppViewContainer"], div[data-testid="stAppViewContainer"] > .main {
                background-color: transparent;
            }
            
            h1, h2, h3 {
                color: marine;
                text-align: center;
                padding-bottom: 10px;
            }
            .texto-pequeno {
                font-size: 18px;
                line-height: 1.5;
                color: #333;
            }

            .stMultiSelect > div[data-baseweb="select"] > div {
                background-color: #FFFFFF;
                border: 1px solid #1c83e1;
            }
            .stButton>button {
                border: 1px solid red;
                border-radius: 5px;
                color: red;
                background-color: transparent;
                padding: 2px 5px;
                transition: box-shadow 0.3s ease-in-out, color 0.3s ease-in-out;
            }

            .stButton>button:hover {
                color: #FF4B4B;
                background-color: white;
                box-shadow: 0 0 15px #ffffff;
            }

            .floating-container {
                position: fixed;
                bottom: 30px;
                right: 30px;
                z-index: 101;
            }

	    .floating-container a {
                display: block;
                padding: 10px 20px;
    		border-radius: 30px;
    		background-color: #FF4B4B;
    		color: white;
    		font-size: 16px;
    		font-weight: bold;
    		text-align: center;
    		text-decoration: none;
    		box-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    		transition: transform 0.2s ease-in-out;
	    }

            .floating-container a:hover {
                transform: scale(1.1);
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)


@st.cache_data
def carregar_dados():
    df_ghs = pd.read_csv('data/GHS.csv')
    df_frases_p = pd.read_csv('data/Frases p.csv')
    
    df_ghs['chave_classificacao_completa'] = df_ghs['Classe de Perigo'].str.strip() + ' ' + df_ghs['Categoria'].astype(str).str.strip()
    return df_ghs, df_frases_p

def processar_classificacoes(lista_de_classificacoes, df_ghs, df_frases_p):
    if not lista_de_classificacoes:
        return None

    dados_filtrados = df_ghs[df_ghs['chave_classificacao_completa'].isin(lista_de_classificacoes)]
    if dados_filtrados.empty:
        st.warning("Nenhuma classificação correspondente foi encontrada.")
        return None

    valores_advertencia = dados_filtrados['Palavra de Advertência'].dropna().unique()
    valores_normalizados = [str(valor).lower().strip() for valor in valores_advertencia]

    palavra_advertencia = "Não aplicável"
    if 'perigo' in valores_normalizados:
        palavra_advertencia = 'PERIGO'
    elif 'atenção' in valores_normalizados:
        palavra_advertencia = 'Atenção'

    pictogramas = dados_filtrados['Pictogramas'].dropna().unique().tolist()

    frases_h = (dados_filtrados['Texto da Frase H']).dropna().unique().tolist()
    
    frases_p_agrupadas = {
        "Prevenção": [], "Resposta a Emergências": [],
        "Armazenamento": [], "Disposição": []
    }
    mapa_colunas_p = {
        'Frases P (Prevenção)': "Prevenção", 'Frases P (Resposta)': "Resposta a Emergências",
        'Frases P (Armazenamento)': "Armazenamento", 'Frases P (Disposição)': "Disposição Final"
    }

    for coluna_original, grupo in mapa_colunas_p.items():
        if coluna_original in dados_filtrados.columns:
            codigos_brutos = dados_filtrados[coluna_original].dropna().tolist()
            codigos_individuais = []
            for entrada in codigos_brutos:
                codigos_separados = str(entrada).split(',')
                for codigo in codigos_separados:
                    codigos_individuais.append(codigo.strip())
            
            codigos_unicos_para_lookup = list(set(codigos_individuais))

            if codigos_unicos_para_lookup:

                frases_do_grupo = df_frases_p[df_frases_p['Codigo_Prec'].isin(codigos_unicos_para_lookup)]['Texto_Prec'].tolist()
                frases_p_agrupadas[grupo] = frases_do_grupo
    
    resultado = {
        'palavra_advertencia': palavra_advertencia, 'pictogramas': pictogramas,
        'frases_h': frases_h, 'frases_p_agrupadas': frases_p_agrupadas
    }
    return resultado


def adicionar_fundo_css_animado():
    img_base64_1 = "data:image/png;base64,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"
    img_base64_2 = "data:image/png;base64,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"
    img_base64_3 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAPoAAAD6CAYAAACI7Fo9AAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAAB3RJTUUH6AYeFRcZckCrjgAAGONJREFUeNrt3XlwlIX9x/Hvc+zmIikGEiHEHBxBJFCHRKKDFjBWggcyQKSlFNB2CEeTmVgKAjUBSilitAEnqCUtCoiUGVA7AuWIBFtRUEYBLQnlCBQKCAmBhJBzP78/6j6/hM2xm+zmePbznnnGGfI8zx7t67mfZ0UYY4wxxlgXCyIREIngN8GYeZHfA5FTECmCSDS/EcbMixzfD8TOmMmREztjXoKc2BnzEuTEzpiXICd2xrwEObEz5iXIiZ0xL0FO7Ix5CXJiZ8xLkBM7Y16CnNgZ8xLkxM6YlyAndsa8BDmxM+YlyImdMS9BTuyMeQlyYmfMS5ATO2OdGvmCBUBGBrEzZmrk9jIziZ0xUyMndsa8BDmxM+YlyImdMS9BTuyMeQlyYmfMS5ATO2NegpzYGfMS5MTOmJcgJ3bGvAQ5sTPmJciJnTEvQU7sjHkJcmJnzEuQEztjXoKc2BnzEuTEzpiXICd2xrwEObEzIvcS5MTOiNxLkBM7I3IvQU7sjMi9BDmxMyL3EuTEzojcS5ATOyNyL0FO7IzIvQQ5sTMi9xLkxM6I3EuQEzsjci+L2BmREzuxMyIndmJnRE7sxM6InNgZI3JiZ0RO5MTOiJzIiZ0ROSN2RuSM2BmREzuxMyIndmJnRE7sxE7kRE7sjMiJnNgZkbuC3GazISsrCyUlJURL7MyMyKurq/H0009DRPDcc88RLLEzs26uJyQkQESgKAr27NlDsMTOzLhPvn//fvzvrQj69OmDsrKyJsctKyvDrl278OmnnxI1sbOuduBt1KhRUFUVmqYhLS2t0XHWrVsHTdMgIti0aRNBEzvrakfXDx06BEVRjE34xtbYjzzyiDHOkSNHnJrv2rVrja2F1mwFHDp0iNiJncjdeQrtJz/5CXRdh6Zp6NevHyorK42/Xbt2zVibi0izm/f127Bhg7Hw2LBhg0vv5/PPP0dsbCzX7MRO5O48T37u3DlYrVaICDRNw6JFi4y/rV+/HqqqQkTwgx/8wOl5btu2DSICXdeRmZnp9HRnzpxBjx49EBERwc14Yidyd7dw4UJjza1pGr766isAwNNPP238+5AhQ5ye39///neICFRVxc9//nOnpikpKUH//v0hIoiOjuY+O7ETubu7efMmevbsCUVRoOs6Bg8ejNLSUvj4+BhgJ0yY4PT8/vGPfxib+8OHD3fqvP7o0aONaVzd3Cd2RuRO9uabbxoH3VRVxciRIw14VqsVv/rVr5ye11dffWVM26NHjxav0Js2bZoxflNH/4md2IncDdXW1iImJsbYJxcRWCwWiAh8fHwa7Lu31MmTJ415KIrS7EG8pUuXGuPGxcWhurqap96Incg92bvvvttgrV5/jf6HP/zB6flcvHjRmFZEcPTo0UbH27hxo/F6AQEBOHPmDM+zEzuRe7qamhqEhYU1QGo/ep6Tk+P0fMrLyxtM//777zuMk5+fD13XjXG2bNnCi2qInchbk7PnveuXnp5ubLLX3/x29QCZHbGu68jKymrwtxMnTiAoKAiKokDTNDz//PO8go7Yiby19evXD5s3b3Zpmry8PIc1uqqqyM3NdWk+3bt3Nzb7Z8+ebfz7lStXcM899xgX6fTv3x+3bt3i5bLETuStzX56bOTIkThx4oTTWwH2/eb6B+VeffVVl147MjLSmP6xxx4DAFRUVCA+Pt7YYrBYLE3uvxM7sRO5i9B1XYeu61i4cKFTa8/o6GiHffTp06e79Nr333+/MX1ERATq6uowYcIE4wIcVVVdOsBH7MRO5E00YcKEBmtnTdMQFhaGDz74oNnpnnzySYe1eu/evWGz2Zx+7cTExAavm56ebsxT13XEx8ejtraW0ImdyNuazWbD8uXLoSiKcbrM/t+kpCScPn260enmzp1rXP9ef/jyyy+dfu1nn33WYWFRf1egoKCAwImdyN3Zzp07ERgY2OBousVigdVqxbJlyxrcsQYAGRkZDtAtFgsWL17s9GvOnDnT4ei9fe2ekZFB2MRO5J7o1KlTGDRoUINz13Z4UVFR2L17tzHuypUrG12jDxgwwOnXW7BggcM8VFXFPffcg4qKCqImdiL3VOXl5UhOTnbYpLYfIJs4cSIuXLiANWvWOCwQ7ENhYaFTr9XUwmLbtm3ETOxE7ulsNhteeeUVqKra4DJX++a5n58fHn300QYPnKi/QHjttdecep1169Y1mL+qqoiJiXHpgJ4zn8XZBQ+xE7vXIK/fvn370L1790b3o1VVbXSNrqoqEhMTnZq//eETbbm6rqVefPFFWCwW/Pvf/yZ2YifypioqKsLQoUOb3ExvbLBarU6di9+xY4fDtKWlpW5776+++ipExKX75Imd2L0Oub2KigpMnTrVaegigh07drQ43z179jhM99///tct7/mdd96BoigICgrCpUuXuM9O7ETubGvWrIGmaY3um9+5H5+amtoq6Hv37m3z+/zwww+N97h+/XoeoCN2Ine1AwcOoEePHo3ut9cfIiMjXd501zQNf/rTn9r0/vbs2WO8t8TERLce2CN2IveqXzUtKirC3Xff3eJ++6lTp5qdz7x58xweXvHyyy+3+n198sknxrX7vr6+OHv2LE+9ETuRt6VPPvmkWeSapmHt2rXNTn/nuXqr1YoVK1a06v0cPHgQ/v7+xjyzs7N5np3YidwdPfXUU02u1TVNw7hx4xqd7saNGwgPD3fY11cUBVu3bnX5feTn58PPzw+apkHXdTzwwAOoq6uD10fsRN5UBQUFWLJkCZYvX47//Oc/Lh9Mqz8EBASgpqbGYbpp06Y1uYA4fvy4S+93586d8PHxMXYBLBYLvv32WyIndiJvrJs3byIlJQWKosBiscBisUDXdUybNq1JfHV1dejZs2ez2O/8XbXt27c3ewDP2YNnhYWFxvu1I9c0DUuXLiVuYifyxtq3bx/69OnT6FrWYrFAURQkJSUhPz/fYdqUlJQmj8BbLBYsWbLEGPfSpUvo3r27w2W18v395/WR2mw2HDhwAG+99RZWrlyJzMxMpKamYuLEiQgNDW3wqGn79IMGDUJVVRVhEzuR16+6uhppaWnGAxibWzPbFwLDhg3D9u3bjX3g9957r8l7yhVFQUJCggF3zJgxTS4UFEUxHuX85ZdfYtCgQcbr2m+XtVqtTb5PVVW79i+sEjuRe6KLFy8iISGhReCNHWQTEcTExGDjxo04e/Zsi+PfuHEDb7zxRpMLBF3XMXbsWABAbm6ucVDNlff061//mpCJncjrd+DAgRb3rVsaVFWFoijG01qbG/eVV16Br69vs+Ps3bvXeNKNqwueiIgI73xKLLETeVNt3769wVo8PDwcgwcPRnBwsMN+rzND/YNhTe2n23+YsakFRkxMDObMmeMycvvr5+XlES+xE3n9Tpw4gUmTJuEvf/mLww0kJ0+eREpKCjRNcxl8Sxib2zLo0aNHswuLOxcc9ul69erFTXZiJ/K2nEsfP358s2tidw7OrMkVRUF0dDReeuklHD582OEZdozYibyVHTx4EA8++GCDg3DuHJxdiCiKgt///vd89DOxE7kn++CDDzBgwAAoitKq/ei2ru15EQyxE3k7VVtbi3Xr1iE0NNQja/emjqg/99xzREjsRN7e3bp1CytXrkS3bt08uv+u6zoef/zxRq+VZ8RO5O1UcXGx8Vx2d4O3WCwYMmRIq37SmRE7kXug06dPY/LkyW47Qq/rOsLCwtz27DjmZdiJ3LOtWrWqzfvuqqoiMDCQt5kSu5HqKnIR2S8i/dyy1FiwQGTlSmH/n7+/vyiK0urpFUURVVXl/fffl/vuu49faGdoyRKRzEx3zS1SRPa7il0l8s5VTU1Nm6CLiKxfv14SExP5ZRK7kU7knQ96W1q1apVMnTq1S33mS5cuydmzZ8XHx0f8/PzE19dX7rrrLrnrrrvMh11EZOlSd2IfrYic5T55F2vFihWN/mCiM/vlc+fO7fSfr7q6Gh9//DF+85vfYNiwYfD392/080yePJn77G7cZ9e5JjfHGj0oKEhWr17daT/XhQsXJCcnR9atWyfFxcUiIhIcHCwPPPCA9O/fX6KiosRiscgbb7wh586dk/nz55t7M76zrNm5Ju+Yfvvb37ZqjR4SEtIpP8+FCxcwffp04265qKgoLF68GJ9++qnDNffHjh2Dqqp4/PHHW5yvKa4N6Oij8UTecdkvnunq0G/fvo2lS5ciICAAIoIRI0Zg27Ztzd5QM2bMGCiKgoMHDzr8zWaz4fDhw1i0aBFiY2Pxy1/+kpvxbcFO5B3bCy+80OWhf/3114iNjYWIoH///ti+fXuL0+zatQsiguTkZOPfKisrsXPnTqSkpCAsLKzB550zZw732VuLncg7vtTU1C4N/Y9//CN8fHygaRpeeuklp54mW1lZiZiYGPj6+uKLL77Axo0bMWnSJHTr1s34fFFRUUhLS8Py5cshIq3+JRpvxa7XQx7x/YG3vjzw1nR9+/aV7777zmPzr6qqktraWpenu3btmnTr1q1Dvxv7e4+KipJNmzbJiBEjnJouKytLTp48KSIiw4cPFwCiKIoMGzZMnnnmGRk3bpz88Ic/FBGRtWvXiojIvffeywN0zR+g2/f9Abrzdx51vy0it9z2xgFTHjC9//77paSkxGPzLywslCtXrghc/P50XZf4+PgO+U5qa2vlm2++kVu3bkliYqJs3bpVgoODnZq2qKhIVqxYISIiFotFRo8ebeAODw93GH/fvn2iqqrTC5EulXvNVH8/NLrpHgKRY27bhJg/n9viLjZ9+vRWXeveUZvuly9fxpAhQ4z9Zldvh50xYwZ++tOfYsuWLbhx40aL5+CDgoIQFxdnvv/hMzLcuel+AiK9WtpPJ/YObMqUKU4/4LGjoV+8eBExMTEQEWRmZro8vc1mQ3V1tdPj7969GyKCxYsXE3lbkBN7x5ecnNyqx0y1N/Tr169j6NChxvPm26NJkyZBRPCvf/2LyNuKnNg7tvHjx7fq1tT2hH779m2MHDkSIoKMjAy3zbegoAArV67Eli1bHH6u+cyZM9B1HT/60Y+I3F3Iib3jGjt2bKeGXltbi4kTJ0JEMHPmTLfuBgQGBhqf585dgZSUFIgIduzYQeTuRE7sHVNiYmKnhj579myICJ555hm3Pjb6s88+a/B5Jk2aZPzt+PHj0HUd8fHxTv8cNJETe6fukUce6bTQc3JyICJ4+OGHUVFR4dZ522w2zJs3D6GhoUhISDD2w202G0aNGgVFUfDPf/6TyD2FnNjbN/sPPXQ26IcPH4aPjw8iIiJw9erVdvs+Vq9eDRHB9OnTidzTyIm9/YqLi+t00IuLixEZGQmr1YrPPvus3b6L48ePw8/PDxEREbh+/TqRtwdyYm+f7BefdBbodXV1eOKJJyAiWLNmTbt9D1evXkXfvn2haRry8/OJvD2RE7vnu/feezsV9KysLIgInn322Xb7DiorK/Hwww9DRLB69Woi7wjkxO7Z+vXr12mgf/vtt/D19UVUVFSLl6e6E7l9C2L27NlE3pHIid1zRUZGtgq6v7+/W49K19TUID4+HqqqYv/+/e2OfMqUKV37V1/NgpzYPdOdD1hwdrD/usuoUaPcAj4zMxMigvT09Hb53NeuXcOoUaOMh0906d+KMxtyYnd/ISEhbvmt9AcffBB5eXmteg9HjhyBxWLBwIED3X6+vKldhL59+0JEMGvWLK7JOyNyYndvwcHBbvsV1das4SsrKxEbGwtd1/H55597/PO+/fbbCAwMhKZpPPDW2ZETu3s6evQofHx83P6zySKC0aNHOwU+NTUVIoJFixZ59LOWlJQgOTkZIoLQ0FDs3r2byLsCcmJv2/7p7Nmzoaqqx34r3Zk1/Ntvvw0RwUMPPeTUs95ak81mw+bNm9G7d2+ICGJjY3H58mUi70rIid31I9tr1qxBUFCQx4DfOdjvdb8T/F//+ldYLBaEhYXh4sWLHvm8x44dM25vtT9cQ1EUPPXUU7h27RqRdyXkxO5ce/fuRUxMTKseMuHqYLVaGyxINE1DVFQUxo4di7/97W94/fXXoWka7r77bhw/ftztn/X06dN4/vnnm3xElq7rCA0Nxccff0zkXfJZd8Te6P/px40b12Bz2l2b5vXnp6oqwsLC8Oijj2Lu3LnIzs7Gjh07cPLkSePxTaWlpfjZz35mPE7Z3U9uKSwsbPAMvOYWaqqqQlEULFy40KXHSxE5sXeqysrKsHDhQlgsFuPnidyxGd6rVy+MHDkSs2bNQlZWFj788EOcOHGi2X1sm82Gbdu2ITw8HCKCMWPGuG3Tubi4GLm5uRgzZkyrnn2naRri4uJw6tQpIif2roPdZrNhw4YNCA0NbXZt7OPj47AAaG6Nr6oqfve737n8fvbv32/cChsQEIDXX3+9zQ9zKC4uxp///GckJSUZ77ktuyQWiwX+/v7YuHEjkRN718B+6NChRtdaISEhiI2NxdixYzFjxgwsWrQI2dnZ2Lx5M/Lz83HgwAFERkY2it1isSA+Pt7pq8dsNht2796NH//4x8YC5Be/+AXOnz/faXA3ddBwypQp7XadPZETe6urq6vDu+++i7y8PHzzzTf47rvvXDrt9tBDDzkcxPLx8UFhYWGL0xcVFSEnJweDBw82tgKSk5NRUFDQqs9SXl6Od955x2O4G9tqsVqtWLVqFZETu7nPs1dWVmLq1KkGKEVRkJOT02CcK1euICcnB8uWLUNqaiqSkpIQHR1tgAkICMCcOXOcWjg01tWrVzF37lzj4Y2ePlOg6zp8fX3xwgsveOxUH5ETe6fcz1+2bBkURcFjjz3msE+9adMmh037AQMGYOrUqdi0aRNKSkpa/do3btzAwIED2wW4pmkICAjA4sWL2/VxVURO7J2qrVu34sKFCw7//vXXX+OJJ54wIA4ePBi5ubm4fft2m19z5syZHj/Pr6oqunfvjuXLl6O0tJQH3oid2JuroKAATz75pLH/3LNnTyxYsKDRhYMz5eXleWwtrigKFEVBcHAwXnvtNZSXl/PougdTOgN2EckTkSFumeH8+SIvv+xVC8zz589Lbm6uvPnmm3L16lXRdV1qa2tFURQBIBaLRcaPHy/z5s2T4cOHOzXPW7duyZAhQ6SoqMjlX3Z1NV9fXwkJCZFevXpJ7969JSwsTEJDQyU0NFR69+4toaGhEhISImFhYRIYGOj5LzQzU2TZMnfNrUD+9/PFl8Xb45q9dUfzd+3ahaSkJJduhhkxYgS2bt3a4j3f7bHJ3tx5dKvV2ugls35+fjh48CDX5MRubuylpaXIzs42jqq7ehmtfVO8b9++yM7ObnST2ZOb7G0dXnzxRSIndvNiLywsRFpaGvz8/Izrwt1xQUpgYCDS0tJQVFRknCuPjo7udNDtP8nksevgiZzYO3LzfO/evUhKSoKiKB65ldUOWtM0TJ482XgYRGcaVFVFUFAQzp07R+TEbh7s9s3zPn36uP0ut644KIqCXbt2ETmxmwP7kSNHMGPGjCYPRHkrcl3X0adPn0aHqKio1m/OEzmxe+oKt5KSEpSUlKCsrAwAUFVVhffeew8JCQnGEWcCd224efMmkRN7+2OvqqrCF198gbfeeguzZs3C6NGjER4e7rCWjoiIQM+ePaEoCtfgbRhcuVGIyIm9TdeDf/TRR5g/fz7i4uIMtKqqcg3dDoNLt9sSObG7crvmRx99hPT0dAwdOtR4koq7H9XMwbnB6bvyiJzYnS09PZ1r6U42HD16lMhbSO9Kb1YRuQqRRHHXtfGrVv3vvy5cG3/ffffJ+PHjG/1baWmpAJC6ujqx2Wwtzqu8vNwY15nxKysrpaqqSkTEqfFramqksrLS6fFtNptUVFR0uRWA/TM2Ga9d7/ibWlq7ZhfeCNMpun79ukvjl5WVSW1trdPjV1RUGAu3pho4cKB069aNyLkZzxthvDLukxM7sRM5kRM7I3IiJ3ZG5IzYGZEzYmdEzoidETkjdkbkjNiJnMiJndiJnMiJndiJnBE7sRM5I3ZG5IzYGZEzYmdEzoidyImcETuREzkjdiIncmIndiJnxE7sRM6IndiJnBE7I3JG7IzIGbETOZEzYidyImfETuSMETuRM0bsRM6IndiJnBE7sRM5I3Zvw07kjNhNjp3IGbGbHDuRM2I3OXYiZ8RucuxEzojd5NiJnBG7ybETOSN2k2MnckbsJsdO5IzYTY6dyBmxmxw7kTNmcuxEzpjJsRM5YybHTuSMmRw7kTNmcuxEzpjJsRM5YybHTuSMmRw7kTNmcuxEzpjJsRM5YybHTuSMmRw7kTNmcuxEzpjJsRM5YybHTuSMmRw7kTNmcuxEzpiJsWdkEDljXoGdyBkjdiJnjNiJnDEvwE7kjJkcO5EzZnLsRM6YybETOWMmx07kjJkcO5EzZnLsRM6YybETOWMmx07kjJkcO5EzZnLsRM6YybETOWMmx07kjJkcO5EzZnLsRM6YybETOWMmxx4KkVB+E4wxxhhjXa3/AxF8IpWHOKqRAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDI0LTA2LTMwVDIxOjIzOjI1KzAwOjAwAcWSVQAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyNC0wNi0zMFQyMToyMzoyNSswMDowMHCYKukAAAAASUVORK5CYII="

    html_animacao = f"""
    <style>
        @keyframes brownian-path-1 {{
            0%   {{ transform: translate(0, 0); opacity: 0; }}
            25%  {{ transform: translate(40px, -60px); opacity: 0.4; }}
            50%  {{ transform: translate(-30px, -120px); opacity: 0.7; }}
            75%  {{ transform: translate(50px, -180px); opacity: 0.4; }}
            100% {{ transform: translate(20px, -250px); opacity: 0; }}
        }}
        @keyframes brownian-path-2 {{
            0%   {{ transform: translate(0, 0); opacity: 0; }}
            25%  {{ transform: translate(-50px, -50px); opacity: 0.5; }}
            50%  {{ transform: translate(20px, -100px); opacity: 0.8; }}
            75%  {{ transform: translate(-40px, -150px); opacity: 0.5; }}
            100% {{ transform: translate(10px, -200px); opacity: 0; }}
        }}
        @keyframes brownian-path-3 {{
            0%   {{ transform: translate(0, 0); opacity: 0; }}
            25%  {{ transform: translate(20px, -80px); opacity: 0.6; }}
            50%  {{ transform: translate(60px, -150px); opacity: 0.9; }}
            75%  {{ transform: translate(-10px, -220px); opacity: 0.6; }}
            100% {{ transform: translate(30px, -300px); opacity: 0; }}
        }}
        
        .background-container {{
            position: fixed; top: 0; left: 0; width: 100%;
            height: 100%; z-index: -1; overflow: hidden;
        }}

        .bubble {{
            position: absolute;
        }}
        .bubble img {{
            opacity: 0.3;
            filter: drop-shadow(0 0 3px rgba(0,0,0,0.3));
        }}

        .b1 {{ top: 70%; left: 10%; animation: brownian-path-1 25s linear infinite; }}
        .b1 img {{ width: 50px; }}

        .b2 {{ top: 80%; left: 25%; animation: brownian-path-2 20s linear 2s infinite; }}
        .b2 img {{ width: 30px; }}

        .b3 {{ top: 60%; left: 40%; animation: brownian-path-3 28s linear 4s infinite; }}
        .b3 img {{ width: 60px; }}

        .b4 {{ top: 85%; left: 55%; animation: brownian-path-1 18s linear 6s infinite; }}
        .b4 img {{ width: 40px; }}
        
        .b5 {{ top: 90%; left: 75%; animation: brownian-path-2 23s linear 8s infinite; }}
        .b5 img {{ width: 55px; }}

        .b6 {{ top: 75%; left: 90%; animation: brownian-path-3 19s linear 5s infinite; }}
        .b6 img {{ width: 35px; }}

    </style>

    <div class="background-container">
        <div class="bubble b1"><img src="{img_base64_1}"></div>
        <div class="bubble b2"><img src="{img_base64_2}"></div>
        <div class="bubble b3"><img src="{img_base64_3}"></div>
        <div class="bubble b4"><img src="{img_base64_1}"></div>
        <div class="bubble b5"><img src="{img_base64_2}"></div>
        <div class="bubble b6"><img src="{img_base64_3}"></div>
    </div>
    """
    st.markdown(html_animacao, unsafe_allow_html=True)
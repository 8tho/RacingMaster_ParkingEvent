<p>このファイルをGoogle Colabなどで実行することにより、理論値を算出できます。<br>
パズルは自力ですが、それ以外の計算過程をこのコードひとつで完了できます。</p>


<h3>書き換えできる項目</h3>

<ul>
  <li><b><code>vehicles</code></b>: 車を定義します。
    <ul>
      <li><b><code>Lafeなど</code></b>: 車種名です。</li>
      <li><b><code>space</code></b>: 1つあたりの車のマスのサイズです。</li>
      <li><b><code>max_count</code></b>: 所有している数です。重複可能上限と定義しています。</li>
      <li><b><code>revenue</code></b>: (基礎の実数で書かれた)収益です。</li>
    </ul>
  </li>
  <br>
  <li><b><code>label</code></b>: (ラベル)A,B,C,Dがあります。特殊効果を定義します。<br>
  ・Aは特殊駐車場マスの特殊効果です。<br>
  ・Bは隣接して駐車する特殊効果です。<br>
  ・CとDは駐車場に同じ車種が存在する場合の特殊効果です。CはAE86の特殊効果,DはFiatの特殊効果を割り当てています。<br>
  ※このラベルは増やせます。レア度をまたいで同じ車種が存在する場合(ここではFiatのようなケース)はラベルを増やして分けます。</li>
  <br>
  <li><b><code>sb_conditions</code></b>: ラベルBのときだけ隣接する車種を指定する必要があるので追加しました。<br>
   ※'FiatLegend','FiatRare' のように同じ車種でもレア度が異なる場合は「,」で複数追加することができます。</li>
  <br>
  <li><b><code>sb</code></b>: SkillBonus(全体収益+x%のx)です。総合収益は<code>(基礎の全体収益)*(SB+100)/100</code>で計算します。</li>
  <br>
  <li><b><code>target_space</code></b>: 解放済みの最大マス数です。</li>
  <br>
  <li><code>if label_a_sb_count < 5:</code> 特殊駐車マスの数です。</li>
  <br>
  <li><code>for i, (combo, total_revenue) in enumerate(combination_total_revenues[:1000], 1):</code><br>
  ↑ここの<code>1000</code>をいじれば上位何件を表示するか変更できます。</li>
</ul>

<hr>

<h3>そのほか</h3>
<ul>
  <li>デイリーバフや特殊イベント(週末20%)は人によって異なるため考慮していません。改造して定義してください。</li>
  <li>分からないこと等あればDMまで。Xのアカウントはクレジットと同じです。</li>
  <li>改造、再配布できます。期間限定イベントなので需要があるのかよく分かりません。</li>
</ul>


<h3>クレジット</h3>
<p>派戸 @Ghx86L</p>

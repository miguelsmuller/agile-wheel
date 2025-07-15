import {
  Component,
  ElementRef,
  ViewChild,
  AfterViewInit,
  Input,
  OnChanges,
  SimpleChanges,
} from '@angular/core';

import { BarChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  PolarComponent,
  GraphicComponent,
} from 'echarts/components';
import * as echarts from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { CallbackDataParams, EChartsOption } from 'echarts/types/dist/shared';

import { ActivityResult } from 'domain/model';

echarts.use([
  TitleComponent,
  TooltipComponent,
  GridComponent,
  PolarComponent,
  BarChart,
  GraphicComponent,
  CanvasRenderer,
]);

@Component({
  selector: 'app-chart-result',
  imports: [],
  templateUrl: './chart-result.component.html',
})
export class ChartResultComponent implements AfterViewInit, OnChanges {
  @Input() result: ActivityResult | null = null;

  @ViewChild('chartContainer', { static: true })
  chartContainer!: ElementRef<HTMLDivElement>;

  private chart!: echarts.ECharts;

  ngAfterViewInit() {
    this.chart = echarts.init(this.chartContainer.nativeElement);

    if (this.result) {
      this.chart.setOption(this.buildOption(this.result));
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['result'] && this.chart && this.result) {
      const options: EChartsOption = this.buildOption(this.result);
      this.chart.setOption(options);
    }
  }

  private buildOption(result: ActivityResult): EChartsOption {
    const maxValue = 5;

    const data = result.dimension_scores.map(ds => ({
      name: ds.dimension.name,
      items: ds.principles.map(p => ({ name: p.principle.name, value: p.average_score })),
    }));

    const flatData = data.flatMap(g => g.items);

    return {
      polar: {},
      angleAxis: {
        type: 'category',
        data: flatData.map(d => d.name),
        z: 0,
        axisLine: { show: false },
        axisTick: { show: false },
        axisLabel: { interval: 0, fontSize: 12, margin: 10, align: 'center' },
      },
      // Eixo dos valores - de dentro pra fora
      radiusAxis: {
        max: maxValue,
        min: 0,
        axisLine: { show: false },
        axisTick: { show: false },
        axisLabel: { show: false },
        splitLine: { show: false },
      },
      series: [
        // Série de fundo (efeito de borda)
        {
          type: 'bar',
          data: Array(flatData.length).fill(maxValue),
          coordinateSystem: 'polar',
          barGap: '-100%',
          z: -1,
          itemStyle: { color: '#e0e0e0', borderColor: '#ccc', borderWidth: 1 },
        },
        // Série principal com cores otimizadas e label destacado
        {
          type: 'bar',
          data: flatData.map(d => d.value),
          coordinateSystem: 'polar',
          barCategoryGap: '8%',
          z: 1,
          label: {
            show: true,
            position: 'insideEnd',
            color: '#FFFFFF',
            fontSize: 18,
            fontWeight: 'bold',
            textShadowBlur: 3,
            textShadowOffsetX: 1,
            textShadowOffsetY: 1,
            formatter: '{c}',
          },
          itemStyle: {
            color: (params: CallbackDataParams): string => {
              const val = Number(params.value);
              const percent = val / maxValue;

              if (percent >= 0.9) return '#2a9d8f';
              if (percent >= 0.7) return '#1f4e5f';
              if (percent >= 0.5) return '#e9c46a';
              if (percent >= 0.3) return '#f4a261';
              return '#e76f51';
            },
          },
        },
      ],
      // Extra Itens
      graphic: [
        {
          type: 'text',
          right: '20',
          top: '50',
          style: {
            text: data[0]?.name ?? '',
            fill: '#444',
            font: 'bold 22px sans-serif',
            align: 'right',
          },
        },
        {
          type: 'text',
          right: '20',
          bottom: '50',
          style: {
            text: data[1]?.name ?? '',
            fill: '#444',
            font: 'bold 22px sans-serif',
            align: 'right',
          },
        },
        {
          type: 'text',
          left: '20',
          bottom: '50',
          style: {
            text: data[2]?.name ?? '',
            fill: '#444',
            font: 'bold 22px sans-serif',
            align: 'left',
          },
        },
        {
          type: 'text',
          left: '20',
          top: '50',
          style: {
            text: data[3]?.name ?? '',
            fill: '#444',
            font: 'bold 22px sans-serif',
            align: 'left',
          },
        },
        /* --- LINHA HORIZONTAL --- */
        {
          type: 'line',
          shape: { x1: 0, y1: '50%', x2: '100%', y2: '50%' },
          style: { stroke: '#bbb', lineWidth: 2 },
          silent: true,
          z: 100,
        },
        /* --- LINHA VERTICAL --- */
        {
          type: 'line',
          shape: { x1: '50%', y1: 0, x2: '50%', y2: '100%' },
          style: { stroke: '#bbb', lineWidth: 2 },
          silent: true,
          z: 100,
        },
      ],
    };
  }
}

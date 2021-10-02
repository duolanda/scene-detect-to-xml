# scene-detect-to-xml
目标是在使用 [PySceneDetect](https://github.com/Breakthrough/PySceneDetect/) 完成镜头分割后，还可以将分割结果以 xml 文件的形式导入到 Premiere 或其他 NLE 软件中进行二次处理、微调，以便更好的辅助镜头语言的研究。



问题：

- 无法兼容 FCPX，目前的解决方案是藉由达芬奇（导入时间线）做中转



TODO：

- [ ] 非整数倍帧率的特殊情况处理
- [ ] 更容易的使用方式（bat or GUI）  
- [ ] 更丰富的阈值或参数调节

